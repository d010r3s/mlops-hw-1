from pathlib import Path

INPUT_DIR = Path("/app/input")
OUTPUT_DIR = Path("/app/output")
WORK_DIR = Path("/app/work")
MODEL_DIR = Path("/app/model")


TEST_CSV = INPUT_DIR / "test.csv"
SAMPLE_SUB_TEMPLATE = INPUT_DIR / "sample_submission.csv"
WORK_LOADED = WORK_DIR / "loaded.parquet"
WORK_META = WORK_DIR / "meta.json"
WORK_PREP = WORK_DIR / "preprocessed.parquet"
WORK_PREDS = WORK_DIR / "preds.npy"
FINAL_SUB = OUTPUT_DIR / "sample_submission.csv"
