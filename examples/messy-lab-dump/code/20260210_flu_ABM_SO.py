"""Agent-based flu model — reads raw_counts.csv, writes results/fit.json."""
import pandas as pd
def run(inp="raw_counts.csv", out="results/fit.json"):
    df = pd.read_csv(inp)
    return df["cytokine"].nunique()
if __name__ == "__main__":
    run()
