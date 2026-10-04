import os
import sys
import time
from pathlib import Path
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"
SUBMISSION_NB_DIR = ROOT / "submission" / "notebooks"

def main():
    SUBMISSION_NB_DIR.mkdir(parents=True, exist_ok=True)
    notebooks = sorted(p for p in NB_DIR.glob("[0-9]*.ipynb"))
    if not notebooks:
        print("No .ipynb notebooks found in notebooks/. Run jupytext first.")
        return 1

    print(f"Executing {len(notebooks)} notebooks and saving to {SUBMISSION_NB_DIR}...")
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")

    for nb_path in notebooks:
        print(f"\n---> Running {nb_path.name}...")
        t0 = time.perf_counter()
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        try:
            ep.preprocess(nb, {"metadata": {"path": str(NB_DIR.resolve())}})
        except Exception as e:
            print(f"ERROR running {nb_path.name}: {e}")
            raise e

        out_path = SUBMISSION_NB_DIR / nb_path.name
        with open(out_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)

        dt = time.perf_counter() - t0
        output_count = sum(len(c.get("outputs", [])) for c in nb.cells)
        print(f"DONE {nb_path.name} in {dt:.1f}s (cells: {len(nb.cells)}, outputs: {output_count})")

    print("\nAll 8 notebooks executed successfully and saved to submission/notebooks/!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
