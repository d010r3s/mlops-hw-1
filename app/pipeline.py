import importlib
from utils import log

STEPS = [
    "scripts.01_load",
    "scripts.02_preprocess",
    "scripts.03_predict",
    "scripts.04_export",
]

def main():
    log("Pipeline start")
    for mod_name in STEPS:
        log(f"Running {mod_name}")
        mod = importlib.import_module(mod_name)
        mod.main()
    log("Pipeline done")

if __name__ == "__main__":
    main()
