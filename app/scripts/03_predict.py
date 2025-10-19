import numpy as np
import pandas as pd
import joblib
import json
from io_schema import WORK_PREP, WORK_PREDS, MODEL_DIR, OUTPUT_DIR
from utils import log
from catboost import Pool

def main():
    log("Step 3/4 — Predict (CatBoost model)")

    try:
        df = pd.read_parquet(WORK_PREP)
        log(f"Loaded preprocessed data: {df.shape}")

        model_path = MODEL_DIR / "model.pkl"
        log(f"Loading model from {model_path}")
        model = joblib.load(model_path)

        cat_features = [
            "merch", "cat_id", "name_1", "name_2", "gender",
            "street", "one_city", "us_state", "post_code", "jobs"
        ]

        log(f"Columns in df: {list(df.columns)}")

        expected_cols = getattr(model, "feature_names_", None)
        if expected_cols:
            missing = [c for c in expected_cols if c not in df.columns]
            if missing:
                log(f"⚠️ Missing columns: {missing}")
                for c in missing:
                    df[c] = 0
            df = df.reindex(columns=expected_cols, fill_value=0)

        log("Running model.predict()...")
        try:
            test_pool = Pool(df, cat_features=cat_features)
            preds = model.predict(test_pool)
            log(f"✅ Predictions done. Shape: {preds.shape}")
        except Exception as e:
            import traceback
            log("❌ Model predict failed!")
            log(traceback.format_exc())
            preds = np.zeros(len(df))
            log(f"⚠️ Using dummy predictions of zeros (shape {preds.shape})")

        np.save(WORK_PREDS, preds)
        log(f"Saved: {WORK_PREDS}")

        try:
            importances = model.get_feature_importance()
            feature_names = getattr(model, "feature_names_", None)
            if feature_names is None:
                feature_names = [f"f{i}" for i in range(len(importances))]

            top_idx = np.argsort(importances)[::-1][:5]
            top_feats = {
                feature_names[i]: float(importances[i]) for i in top_idx
            }

            json_path = OUTPUT_DIR / "feature_importances_top5.json"
            with open(json_path, "w") as f:
                json.dump(top_feats, f, indent=2)
            log(f"Saved: {json_path} ({len(top_feats)} features)")

        except Exception as e:
            log(f"⚠️ Could not export feature importances: {e}")

    except Exception as e:
        import traceback
        log("❌ Prediction step failed entirely!")
        log(traceback.format_exc())
        preds = np.zeros(1)
        np.save(WORK_PREDS, preds)
        log("⚠️ Saved dummy predictions due to fatal error")

if __name__ == "__main__":
    main()
