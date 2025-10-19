import pandas as pd
from io_schema import WORK_LOADED, WORK_PREP
from utils import log

def main():
    log("Step 2/4 — Preprocess (pass-through baseline)")
    df = pd.read_parquet(WORK_LOADED)
    df.to_parquet(WORK_PREP, index=False)
    log(f"Saved: {WORK_PREP}")

if __name__ == "__main__":
    main()
