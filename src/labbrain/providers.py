"""Vision-provider seam for fixture, Claude Science, and Anthropic runtimes."""

from __future__ import annotations

import base64
import importlib
import importlib.util
import inspect
import json
import os
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Protocol

from .schema import PanelExtraction


class VisionProvider(Protocol):
    """A blind reader of one cropped figure panel."""

    name: str

    def extract_panel(self, image_path: str, context: dict) -> PanelExtraction: ...


def _slug_component(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _panel_tool() -> dict[str, Any]:
    point_schema = {
        "type": "object",
        "properties": {
            "x": {"type": "string"},
            "y": {"type": "number"},
            "y_unit": {"type": "string"},
        },
        "required": ["x", "y"],
        "additionalProperties": False,
    }
    return {
        "name": "report_panel_extraction",
        "description": "Report a blind quantitative read of exactly one figure panel.",
        "input_schema": {
            "type": "object",
            "properties": {
                "chart_type": {
                    "type": "string",
                    "enum": [
                        "bar",
                        "box",
                        "dose_response",
                        "kaplan_meier",
                        "kinetics",
                        "unknown",
                    ],
                },
                "x_axis_label": {"type": "string"},
                "y_axis_label": {"type": "string"},
                "y_min": {"type": ["number", "null"]},
                "y_max": {"type": ["number", "null"]},
                "series_label": {"type": "string"},
                "points": {"type": "array", "items": point_schema, "maxItems": 500},
                "peak_value": {"type": ["number", "null"]},
                "peak_x": {"type": ["string", "null"]},
                "confidence": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                },
                "reader_notes": {"type": "string"},
                "flags": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["broken_axis", "busy", "log_scale"],
                    },
                },
            },
            "required": [
                "chart_type",
                "x_axis_label",
                "y_axis_label",
                "y_min",
                "y_max",
                "series_label",
                "points",
                "peak_value",
                "peak_x",
                "confidence",
                "reader_notes",
                "flags",
            ],
            "additionalProperties": False,
        },
    }


def _reader_prompt(context: Mapping[str, Any]) -> str:
    hints = {
        key: context[key]
        for key in (
            "caption",
            "figure_id",
            "panel_id",
            "series_hint",
            "chart_type_hint",
            "y_axis_hint",
        )
        if context.get(key) not in (None, "")
    }
    return (
        "Read only the attached cropped scientific figure panel. Do not infer values "
        "from paper body text. Report the axis minimum and maximum, the requested "
        "series and its per-x values, the peak, and honest confidence. Add any of "
        "broken_axis, busy, or log_scale that apply. Use the "
        "report_panel_extraction tool. Panel context:\n"
        + json.dumps(hints, ensure_ascii=False, indent=2)
    )


def _image_source(image_path: str | Path) -> dict[str, str]:
    encoded = base64.b64encode(Path(image_path).read_bytes()).decode("ascii")
    return {"type": "base64", "media_type": "image/png", "data": encoded}


def _panel_from_mapping(payload: Mapping[str, Any]) -> PanelExtraction:
    """Construct the fixed dataclass while leaving coercion to extract.py."""
    return PanelExtraction(
        chart_type=payload.get("chart_type", "unknown"),
        x_axis_label=payload.get("x_axis_label", ""),
        y_axis_label=payload.get("y_axis_label", ""),
        y_min=payload.get("y_min"),
        y_max=payload.get("y_max"),
        series_label=payload.get("series_label", ""),
        points=payload.get("points", []),
        peak_value=payload.get("peak_value"),
        peak_x=payload.get("peak_x"),
        confidence=payload.get("confidence", "medium"),
        reader_notes=payload.get("reader_notes", ""),
        flags=payload.get("flags", []),
    )


def _mapping_from_response(response: Any) -> Mapping[str, Any]:
    """Find tool input across dict-based and SDK-object response shapes."""
    extraction_keys = {"chart_type", "points", "series_label"}
    seen: set[int] = set()

    def visit(value: Any) -> Mapping[str, Any] | None:
        identity = id(value)
        if identity in seen:
            return None
        seen.add(identity)

        if isinstance(value, Mapping):
            if extraction_keys <= set(value):
                return value
            for key in ("input", "tool_input", "output", "result", "data", "content"):
                if key in value:
                    found = visit(value[key])
                    if found is not None:
                        return found
            for nested in value.values():
                found = visit(nested)
                if found is not None:
                    return found
            return None

        if isinstance(value, (list, tuple)):
            for nested in value:
                found = visit(nested)
                if found is not None:
                    return found
            return None

        if isinstance(value, str):
            candidate = value.strip()
            if candidate.startswith("```"):
                candidate = re.sub(r"^```(?:json)?\s*|\s*```$", "", candidate)
            try:
                return visit(json.loads(candidate))
            except (json.JSONDecodeError, TypeError):
                return None

        for attribute in ("input", "tool_input", "output", "result", "data", "content"):
            if hasattr(value, attribute):
                found = visit(getattr(value, attribute))
                if found is not None:
                    return found
        return None

    payload = visit(response)
    if payload is None:
        raise RuntimeError("Vision provider returned no report_panel_extraction tool payload.")
    return payload


class FixtureProvider:
    """Deterministic provider backed by one JSON file per configured panel."""

    name = "fixture"

    def __init__(self, fixtures_dir: str | Path = "tests/fixtures") -> None:
        self.fixtures_dir = Path(fixtures_dir)

    def extract_panel(self, image_path: str, context: dict) -> PanelExtraction:
        del image_path  # The deterministic fixture is keyed solely by panel identity.
        figure = _slug_component(context.get("figure_id", ""))
        panel = _slug_component(context.get("panel_id", ""))
        fixture_path = self.fixtures_dir / f"{figure}_{panel}.json"
        if not fixture_path.is_file():
            raise FileNotFoundError(
                f"No fixture extraction for {context.get('figure_id', '')}"
                f"{context.get('panel_id', '')}: {fixture_path}"
            )
        try:
            payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid fixture JSON: {fixture_path}: {exc}") from exc
        if not isinstance(payload, Mapping):
            raise RuntimeError(f"Fixture must contain a JSON object: {fixture_path}")
        return _panel_from_mapping(payload)


class HostLLMProvider:
    """Claude Science provider using the host.llm runtime exposed by the host app."""

    name = "hostllm"

    def __init__(self) -> None:
        try:
            self._host_llm = importlib.import_module("host.llm")
        except (ImportError, ModuleNotFoundError) as exc:
            raise RuntimeError(
                "host.llm is unavailable. Run under Claude Science or use "
                "--provider fixture."
            ) from exc

    def extract_panel(self, image_path: str, context: dict) -> PanelExtraction:
        tool = _panel_tool()
        prompt = _reader_prompt(context)
        source = _image_source(image_path)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "source": source},
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        response = self._invoke(
            prompt=prompt,
            image_path=str(image_path),
            image=source,
            messages=messages,
            tools=[tool],
            tool_schema=tool,
            context=context,
        )
        return _panel_from_mapping(_mapping_from_response(response))

    def _invoke(self, **kwargs: Any) -> Any:
        messages_api = getattr(self._host_llm, "messages", None)
        create = getattr(messages_api, "create", None)
        if callable(create):
            return create(
                max_tokens=4096,
                tools=kwargs["tools"],
                tool_choice={"type": "tool", "name": "report_panel_extraction"},
                messages=kwargs["messages"],
            )

        for name in ("extract", "invoke", "complete", "generate", "chat"):
            candidate = getattr(self._host_llm, name, None)
            if callable(candidate):
                return _call_with_supported_kwargs(candidate, kwargs)
        if callable(self._host_llm):
            return _call_with_supported_kwargs(self._host_llm, kwargs)
        raise RuntimeError(
            "host.llm exposes no supported callable (messages.create, extract, invoke, "
            "complete, generate, or chat)."
        )


def _call_with_supported_kwargs(function: Any, kwargs: dict[str, Any]) -> Any:
    try:
        signature = inspect.signature(function)
    except (TypeError, ValueError):
        return function(**kwargs)
    accepts_kwargs = any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in signature.parameters.values()
    )
    selected = kwargs if accepts_kwargs else {
        key: value for key, value in kwargs.items() if key in signature.parameters
    }
    if not selected:
        raise RuntimeError("host.llm callable accepts none of the required vision inputs.")
    return function(**selected)


class AnthropicProvider:
    """Direct Anthropic Messages API provider, imported only when requested."""

    name = "anthropic"

    def __init__(self, model: str = "claude-opus-4-8") -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is required for --provider anthropic; "
                "use --provider fixture for offline operation."
            )
        try:
            anthropic = importlib.import_module("anthropic")
        except (ImportError, ModuleNotFoundError) as exc:
            raise RuntimeError(
                "The anthropic SDK is not installed; use --provider fixture or install it."
            ) from exc
        self.model = model
        self._client = anthropic.Anthropic(api_key=api_key)

    def extract_panel(self, image_path: str, context: dict) -> PanelExtraction:
        tool = _panel_tool()
        response = self._client.messages.create(
            model=self.model,
            max_tokens=4096,
            tools=[tool],
            tool_choice={"type": "tool", "name": "report_panel_extraction"},
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "source": _image_source(image_path)},
                        {"type": "text", "text": _reader_prompt(context)},
                    ],
                }
            ],
        )
        return _panel_from_mapping(_mapping_from_response(response))


def _host_llm_available() -> bool:
    try:
        return importlib.util.find_spec("host.llm") is not None
    except (ImportError, ModuleNotFoundError, AttributeError, ValueError):
        return False


def get_provider(name: str = "auto", **kwargs: Any) -> VisionProvider:
    """Resolve a named provider, preferring local host runtime in auto mode."""
    normalized = name.strip().lower().replace("_", "").replace("-", "")
    if normalized == "auto":
        if _host_llm_available():
            return HostLLMProvider()
        if os.environ.get("ANTHROPIC_API_KEY"):
            return AnthropicProvider(model=kwargs.get("model", "claude-opus-4-8"))
        return FixtureProvider(kwargs.get("fixtures_dir", "tests/fixtures"))
    if normalized == "fixture":
        return FixtureProvider(kwargs.get("fixtures_dir", "tests/fixtures"))
    if normalized in {"host", "hostllm"}:
        return HostLLMProvider()
    if normalized == "anthropic":
        return AnthropicProvider(model=kwargs.get("model", "claude-opus-4-8"))
    raise ValueError(
        f"Unknown provider '{name}'. Choose auto, fixture, hostllm, or anthropic."
    )

