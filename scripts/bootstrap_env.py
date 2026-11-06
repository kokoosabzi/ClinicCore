"""Create a private .env for a fresh local installation.

Existing .env files are intentionally never overwritten.
"""
from __future__ import annotations

import secrets
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"


def main() -> int:
    if ENV_FILE.exists():
        print("Existing .env found; leaving it unchanged.")
        return 0

    secret_key = secrets.token_urlsafe(48)
    admin_password = secrets.token_urlsafe(24)
    content = (
        "# Generated locally by scripts/bootstrap_env.py; do not commit.\n"
        "DATABASE_URL=sqlite:///./data/cliniccore.db\n"
        f"SECRET_KEY={secret_key}\n"
        "ADMIN_USERNAME=admin\n"
        f"ADMIN_PASSWORD={admin_password}\n"
    )

    try:
        with ENV_FILE.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
    except FileExistsError:
        print("Another process created .env; leaving it unchanged.")
        return 0

    print("Created a private local .env file.")
    print("Initial administrator username: admin")
    print(f"Initial administrator password (shown once): {admin_password}")
    print("Change this password after the first login.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
