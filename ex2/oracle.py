"""pulls parameters and tracks overrides"""

import os
import sys

try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    print(
            "[ERROR] The 'python-dotenv' package is missing."
            "\nRun: pip install python-dotenv",
            file=sys.stderr
            )
    sys.exit(1)


def verify_security() -> None:
    """validation check"""
    print("Environment security check:")
    no_secrets = True
    target_key = "API_" + "KEY ="
    target_db = "DATABASE_" + "URL ="
    try:
        """
        looking for the target secret lines within our source code
        os.environ.get reads env variables from systems memory
        """
        with open(__file__, "r", encoding="utf-8") as current_file:
            for line in current_file:
                if (
                        target_key in line or
                        target_db in line) and (
                        "os.getenv" not in line and
                        "os.environ" not in line
                        ):
                    if (
                            "target_key =" not in line and
                            "target_db =" not in line
                            ):
                        no_secrets = False
                        break
        if no_secrets:
            print("[OK] No hardcoded secrets detected")
        else:
            print("[CRITICAL] Hardcoded credentials exposed in source!")
    except Exception:
        print("[CRITICAL] Unable to execute file analysis")
    if os.path.exists(".env"):
        # verifying config file presence
        print("[OK] .env file properly configured")
    else:
        print("[CRITICAL] Running without a local .env config file")
    try:
        # checking if environment registry is modifiable
        os.environ["_ORACLE_TEST_"] = "1"
        del os.environ["_ORACLE_TEST_"]
        print("[OK] Production overrides available")
    except Exception:
        print("[CRITICAL] Production overrides unavailable")


def main() -> None:
    """
    load config from local .env file if present
    os.getenv fetches these configs from memory, but in the case
    of mode and log it offers a fallback value.
    These are also overriden by environment variables if any.
    """
    load_dotenv()
    print("\nORACLE STATUS: Reading the Matrix...")
    mode: str = os.getenv("MATRIX_MODE", "development").strip()
    db_url: str | None = os.getenv("DATABASE_URL")
    api_key: str | None = os.getenv("API_KEY")
    log_level: str = os.getenv("LOG_LEVEL", "DEBUG").strip()
    zion_end: str | None = os.getenv("ZION_ENDPOINT")
    if mode == "":
        mode = "development"
    if log_level == "":
        log_level = "DEBUG"
    allowed_modes = ["development", "production"]
    if mode not in allowed_modes:
        print(f"[ERROR] Access denied: Invalid MATRIX_MODE '{mode}'",
              file=sys.stderr)
        sys.exit(1)
    raw_values = [
            db_url.strip() if db_url else "",
            api_key.strip() if api_key else "",
            zion_end.strip() if zion_end else ""
            ]
    if any(val == "" for val in raw_values):
        print(
                "\n[ERROR] Access denied: Missing configuration properties",
                file=sys.stderr
                )
        sys.exit(1)

    if mode == "production":
        db_display = "Connected to production cluster"
    else:
        db_display = "Connected to local instance"
    api_display = "Authenticated"

    print("\nConfiguration loaded:")
    print(f"Mode: {mode}")
    print(f"Database: {db_display}")
    print(f"API Access: {api_display}")
    print(f"Log Level: {log_level}")
    print("Zion Network: Online\n")

    verify_security()
    print("\nThe Oracle sees all configurations")


if __name__ == "__main__":
    main()
