"""querying local metadata versions, handles missing packages and sims data"""

import importlib.metadata
import sys


def check_dependencies() -> bool:
    """verifies available packes"""
    packages = {
            "pandas": "Data manipulation ready",
            "numpy": "Numerical computation ready",
            "requests": "Network access ready",
            "matplotlib": "Visualization ready",
            }
    print("\nChecking dependencies:")
    all_available = True
    missing_packages = []
    for pkg, desc in packages.items():
        try:
            version = importlib.metadata.version(pkg)
            print(f"[OK] {pkg} ({version}) - {desc}")
        except importlib.metadata.PackageNotFoundError:
            print(f"[MISSING] {pkg} - Required dependency is not installed!")
            missing_packages.append(pkg)
            all_available = False
    if not all_available:
        print(
                "\n[ERROR] Missing required simulation modules.",
                file=sys.stderr
                )
        print(
                "\n--- DEPENDENCY MANAGEMENT INSTRUCTIONS ---",
                file=sys.stderr
                )
        print(
                "To fix using pip (Requirements file framework):",
                file=sys.stderr
                )
        print(
                " pip install -r requirements.txt",
                file=sys.stderr
                )
        print(
                "\nTo fix using Poetry (Deterministic lockfile environment):",
                file=sys.stderr
                )
        print(
                " poetry install",
                file=sys.stderr
                )
        print(
                " petry run python loading.py",
                file=sys.stderr
                )
        print(
                "----------------------------------------",
                file=sys.stderr
                )
    return all_available


def run_simulation() -> None:
    """sims 1000 matrix data points"""
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    print("\nAnalyzing Matrix data...")
    print("Processing 1000 data points...")

    time_series = np.linspace(0, 10, 1000)
    matrix_noise = np.random.normal(0, 1, 1000)
    signal = np.sin(time_series) + matrix_noise

    df = pd.DataFrame({"Time": time_series, "Signal": signal})

    print("Generating visualization...")
    plt.figure(figsize=(10, 6))
    plt.plot(df["Time"], df["Signal"], color="green", alpha=0.6,
             label="Matrix Code Stream")
    plt.title("Zion Mainframe - Matrix Signal Analysis")
    plt.xlabel("Timeline Vector")
    plt.ylabel("Frequency Amplitude")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    output_file = "matrix_analysis.png"
    plt.savefig(output_file)
    plt.close()

    print("\nAnalysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> None:
    print("\nLOADING STATUS: Loading programs...")
    if not check_dependencies():
        sys.exit(1)
    try:
        run_simulation()
    except Exception as e:
        print(f"CRITICAL: Failed to exeute simulation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
