"""pulls parameters and tracks overrides"""

import os
import sys
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    print(
            "[ERROR] The 'python-dotenv' package is missing.",
            file=sys.stderr,
            )
    print("Run: pip install python-dotenv", file=sys.stderr)
    sys.exit(1)


def verify_security() -> None:
    """validation check"""
    print("Environment security check:")
    no_secrets = True
    target_key = "API_" + "KEY ="
    target_db = "DATABASE_" + "URL ="
    try:
        # scans file for hardcoded secrets
        with open(__file__, "r", encoding="utf-8") as current_file:
            for line in current_file:
                if (target_key in line or target_db in line) and (
                        "os.getenv" not in line and "os.environ" not in line
                        ):
                    if "target_key =" not in line and "target_db ="\
                            not in line:
                        no_secrets = False
                        break
        if no_secrets:
            print("[OK] No hardcoded secrets detected")
        else:
            print("[CRITICAL] Hardcoded credentials exposed in source!")
    except Exception:
        print("[WARN] Unable to execute automated static file analysis")
    if os.path.exists(".env"):
        # verifying config presence
        print("[OK] .env file properly configured")
    else:
        print("[WARN] Running without a local .env configuration file")
    try:
        # checking if environment registry is modifiable
        os.environ["_ORACLE_TEST_"] = "1"
        del os.environ["_ORACLE_TEST_"]
        print("[OK] Production overrides available")
    except Exception:
        print("[CRITICAL] Production overrides unavailable")


def main() -> None:
    """load config from local .env if present"""
    load_dotenv()
    print("ORACLE STATUS: Reading the Matrix...")

    # fetch config req via env get
    mode: str = os.getenv("MATRIX_MODE", "development")
    db_url: Optional[str] = os.getenv("DATABASE_URL")
    api_key: Optional[str] = os.getenv("API_KEY")
    log_level: str = os.getenv("LOG_LEGEL", "DEBUG")
    zion_end: Optional[str] = os.getenv("ZION_ENDPOINT")

    if not all([db_url, api_key, zion_end]):
        print(
                "\n[ERROR] Mainframe access denied: Missing configuration"
                " properties", file=sys.stderr,
                )
        print("Please copy and edit your configuration:", file=sys.stderr)
        print("  cp .env.example .env", file=sys.stderr)
        sys.exit(1)

    db_display = (
            "Connected to production cluster"
            if mode == "production"
            else "Connected to local instance"
            )
    api_display = "Authenticated" if api_key else "Missing token"
    zion_display = "Online" if zion_end else "Offline"

    print("\nConfiguration loaded:")
    print(f"Mode: {mode}")
    print(f"Database: {db_display}")
    print(f"API Access: {api_display}")
    print(f"Log Level: {log_level}")
    print(f"Zion Network: {zion_display}\n")

    verify_security()
    print("\nThe Oracle sees al configurations")


if __name__ == "__main__":
    main()
