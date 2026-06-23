"""script for global and virtual env info"""

import sys
import os


def is_virtual_env() -> bool:
    """
    detects virtual env by comparison of these 2 installation
    internal paths.
    1 base - python installation on OS
    2 .prefix points to where python is currently executed
    """
    return sys.prefix != sys.base_prefix


def get_package_path() -> str:
    """Looking up from sys.path the site packages dir"""
    try:
        paths = [
                p for p in sys.path if "site-packages" in p
                ]
        if paths:
            return paths[0]
    except Exception:
        pass
    return "Unknown path configuration"


def main() -> None:
    """monitoring loop verifying env config"""
    current_python: str = sys.executable
    if not is_virtual_env():
        print("MATRIX STATUS: You're still plugged in")
        print(f"\nCurrent Python: {current_python}")
        print("Virtual Enviromment: None detected")
        print("\nWARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print("\nTo enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print(r"matrix_env\Scripts\activate # On Windows")
        print("\nThen run this program again.")
    else:
        env_path: str = sys.prefix
        print("MATRIX STATUS: Welcome to the construct")
        print(f"\nCurrent Python: {current_python}")
        print(f"Virtual Environment: {os.path.basename(env_path)}")
        print(f"Environment Path: {env_path}")
        print("\nSUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print("\nPackage installation path:")
        print(get_package_path())


if __name__ == "__main__":
    main()
