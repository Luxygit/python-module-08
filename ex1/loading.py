"""
querying local metadata versions, handles missing packages and sims data
for pip:
python -m venv matrix
source matrix/bin/activate
pip install -r requirements.txt
for poetry:
poetry init
poetry add x xx xx
poetry run python loading.py
"""

import importlib
import sys


def check_dependencies() -> bool:
    """verifies available packages in the venv"""
    packages = {
            "pandas": "Data manipulation ready",
            "numpy": "Numerical computation ready",
            "matplotlib": "Visualization ready",
            }
    print("\nChecking dependencies:")
    all_available: bool = True
    metadata = importlib.import_module("importlib.metadata")
    missing_packages: list[str] = []
    for pkg, desc in packages.items():
        try:
            """checking site-packages dir for package metadata"""
            version = metadata.version(pkg)
            print(f"[OK] {pkg} ({version}) - {desc}")
        except Exception:
            print(f"[MISSING] {pkg} - Required dependency is not installed!")
            missing_packages.append(pkg)
            all_available = False
    if not all_available:
        print(
                "\n[ERROR] Missing required simulation modules."
                "\n--- DEPENDENCY MANAGEMENT INSTRUCTIONS ---"
                "\nTo fix using pip (requirements.txt file):"
                "\n pip install -r requirements.txt"
                "\nTo fix using Poetry (lockfile env):"
                "\n poetry install"
                "\n poetry run python loading.py"
                "\n----------------------------------------",
                file=sys.stderr
                )
    return all_available


def run_simulation() -> None:
    """
    sims 1000 matrix data points with
    numpy.linspace as the timeline vector
    np.random gives 1000 numbers between 0 and 1
    np.sin calcs a wave of every number in the passed timeline array
    and at the same time adds each sin index to the random noise index
    df.DataFrame constructs a new matrix table that takes a dict
    with time (horizontal) and signal(vertical) keys
    plt.figure opens a blank canvas 6x10
    .plot is passed X Y coords
    .title . xlabel & ylabel are just labels
    .grid adds a background layou
    .savefig saves the drawing to a file
    .close frees up space allocation of the canvas
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd  # type: ignore

    print("\nAnalyzing Matrix data...\nProcessing 1000 data points...")
    time_series = np.linspace(0, 10, 1000)
    matrix_noise = np.random.normal(0, 1, 1000)
    signal = np.sin(time_series) + matrix_noise
    df = pd.DataFrame({"Time": time_series, "Signal": signal})
    print("Generating visualization...")
    plt.figure(figsize=(10, 6))
    plt.plot(df["Time"], df["Signal"], color="green", alpha=0.6,
             label="Matrix Stream")
    plt.title("Matrix Signal Analysis")
    plt.xlabel("Timeline Vector")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle="--", alpha=0.5)
    output_file = "matrix_analysis.png"
    plt.savefig(output_file)
    plt.close()
    print("\nAnalysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> None:
    """
    if check_dependencies returns false because some
    dependencies are missing the program shows errors and exits
    Otherwise we try to run it
    """
    print("\nLOADING STATUS: Loading programs...")
    if not check_dependencies():
        sys.exit(1)
    try:
        run_simulation()
    except Exception as e:
        print(f"CRITICAL: Failed to execute simulation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
