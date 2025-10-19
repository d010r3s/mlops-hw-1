import numpy as np
import pandas as pd
from io_schema import WORK_PREP, WORK_PREDS, WORK_META, FINAL_SUB, SAMPLE_SUB_TEMPLATE
from utils import log, load_json
from pathlib import Path
import matplotlib.pyplot as plt
import json
import os
def main():
    log("Step 4/4 — Export submission")
    if not os.path.exists(WORK_PREP):
        log(f"❌ Missing preprocessed data: {WORK_PREP}")
        return
    if not os.path.exists(WORK_PREDS):
        log(f"❌ Missing predictions file: {WORK_PREDS}")
        return
    meta = load_json(WORK_META)
    id_col = meta.get("id_col")
    sub_cols = meta.get("sub_cols")

    df = pd.read_parquet(WORK_PREP)
    preds = np.load(WORK_PREDS)

    if sub_cols:
        sub = pd.read_csv(SAMPLE_SUB_TEMPLATE)
        pred_cols = [c for c in sub.columns if c != id_col]
        pred_col = pred_cols[-1] if pred_cols else "prediction"
        sub[pred_col] = preds[: len(sub)]
    else:
        if id_col in df.columns:
            sub = pd.DataFrame({id_col: df[id_col].values, "prediction": preds})
        else:
            sub = pd.DataFrame({"prediction": preds})

    Path(FINAL_SUB).parent.mkdir(parents=True, exist_ok=True)
    sub.to_csv(FINAL_SUB, index=False)
    log(f"Saved: {FINAL_SUB} (shape {sub.shape})")

    plt.figure(figsize=(6, 4))
    plt.hist(preds, bins=40, color="gray", alpha=0.7)
    plt.title("Predictions distribution")
    plt.tight_layout()
    plt.savefig("/app/output/preds_density.png", dpi=150)
    plt.close()
    log("Saved: preds_density.png")

    log("Export finished")

if __name__ == "__main__":
    main()
