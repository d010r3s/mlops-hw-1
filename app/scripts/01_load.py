import pandas as pd
from pathlib import Path
from io_schema import TEST_CSV, SAMPLE_SUB_TEMPLATE, WORK_LOADED, WORK_META
from utils import log, read_csv_strict, save_json

def main():
    log("Step 1/4 — Load test.csv")
    df = read_csv_strict(TEST_CSV)
    log(f"Loaded test.csv with shape {df.shape}")

    id_col = None
    for cand in ["id", "ID", "Id"]:
        if cand in df.columns:
            id_col = cand
            break
    if id_col is None:
        id_col = df.columns[0]

    sub_cols = None
    if SAMPLE_SUB_TEMPLATE.exists():
        sub_df = pd.read_csv(SAMPLE_SUB_TEMPLATE, nrows=5)
        sub_cols = list(sub_df.columns)
        log(f"Found sample_submission template with columns: {sub_cols}")

    WORK_LOADED.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(WORK_LOADED, index=False)
    save_json(WORK_META, {"id_col": id_col, "sub_cols": sub_cols})

    log(f"Saved: {WORK_LOADED} and meta.json")

if __name__ == "__main__":
    main()
