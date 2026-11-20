"""End-to-end smoke test for a fresh Windows installation and restart.

This script is invoked by Windows CI after setup.bat/start.bat. It deliberately
uses only the Python standard library so the installed runtime is tested without
extra test-client shortcuts.
"""
from __future__ import annotations

import argparse
import http.cookiejar
import json
import secrets
import sys
from datetime import date, datetime, time, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
STATE_FILE = DATA_DIR / "windows-smoke-state.json"
BASE_URL = "http://127.0.0.1:8000"


class HiddenCsrfParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.token: str | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != "input":
            return
        values = dict(attrs)
        if values.get("name") == "csrf_token":
            self.token = values.get("value")


class RuntimeClient:
    def __init__(self) -> None:
        cookies = http.cookiejar.CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(cookies))

    def request(self, path: str, *, method: str = "GET", data: bytes | None = None,
                content_type: str | None = None) -> tuple[int, str, bytes]:
        headers = {"User-Agent": "ClinicCore-Windows-Smoke/1.0"}
        if content_type:
            headers["Content-Type"] = content_type
        request = Request(BASE_URL + path, data=data, headers=headers, method=method)
        try:
            with self.opener.open(request, timeout=20) as response:
                return response.status, response.geturl(), response.read()
        except HTTPError as error:
            return error.code, error.geturl(), error.read()
        except URLError as error:
            raise RuntimeError(f"Cannot reach {BASE_URL}{path}: {error}") from error

    @staticmethod
    def csrf_token(html: bytes) -> str:
        parser = HiddenCsrfParser()
        parser.feed(html.decode("utf-8", errors="replace"))
        if not parser.token:
            raise RuntimeError("CSRF token was not rendered in the form.")
        return parser.token

    def login(self, username: str, password: str, *, first_login: bool,
              replacement_password: str | None = None) -> str:
        status, url, html = self.request("/login")
        if status != 200:
            raise RuntimeError(f"Login form returned HTTP {status}.")
        token = self.csrf_token(html)
        body = urlencode({
            "username": username,
            "password": password,
            "csrf_token": token,
        }).encode()
        status, url, html = self.request(
            "/login", method="POST", data=body,
            content_type="application/x-www-form-urlencoded",
        )
        if status != 200:
            raise RuntimeError(f"Login submission returned HTTP {status}: {html[:500]!r}")
        if first_login:
            if not url.endswith("/change-password"):
                raise RuntimeError(f"Fresh admin was not forced to change password (landed at {url}).")
            token = self.csrf_token(html)
            new_password = replacement_password or secrets.token_urlsafe(24)
            body = urlencode({
                "password": new_password,
                "confirm": new_password,
                "csrf_token": token,
            }).encode()
            status, url, html = self.request(
                "/change-password", method="POST", data=body,
                content_type="application/x-www-form-urlencoded",
            )
            if status != 200 or not url.endswith("/dashboard"):
                raise RuntimeError(f"First-login password change failed: HTTP {status}, {url}.")
            return new_password
        if not url.endswith("/dashboard"):
            raise RuntimeError(f"Existing admin login did not reach dashboard: {url}.")
        return password

    def json_request(self, path: str, *, method: str = "GET", payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        status, url, body = self.request(
            path, method=method, data=data,
            content_type="application/json" if data is not None else None,
        )
        if status < 200 or status >= 300:
            raise RuntimeError(f"{method} {path} returned HTTP {status}: {body[:1000]!r}")
        return json.loads(body.decode("utf-8")) if body else None


def read_env_file() -> dict[str, str]:
    values: dict[str, str] = {}
    env_path = ROOT / ".env"
    if not env_path.is_file():
        raise RuntimeError("Fresh setup did not create .env.")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def create_records() -> None:
    env = read_env_file()
    username = env.get("ADMIN_USERNAME", "admin")
    password = env.get("ADMIN_PASSWORD", "")
    if not password or password == "admin":
        raise RuntimeError("Fresh setup did not generate a non-default administrator password.")

    client = RuntimeClient()
    changed_password = client.login(username, password, first_login=True)
    status, url, dashboard = client.request("/dashboard")
    if status != 200:
        raise RuntimeError(f"Dashboard did not render after first login: HTTP {status}.")

    national_code = str(secrets.randbelow(10**10)).zfill(10)
    patient = client.json_request(
        "/patients/", method="POST",
        payload={
            "first_name": "Windows",
            "last_name": "Smoke",
            "national_code": national_code,
            "phone": "09120000000",
            "notes": "Automated Windows installation and persistence check",
        },
    )
    patient_id = int(patient["id"])

    starts_on = date.today() + timedelta(days=1)
    while starts_on.isoweekday() == 5:
        starts_on += timedelta(days=1)
    appointment_start = datetime.combine(starts_on, time(11, 0))
    appointment = client.json_request(
        "/appointments/", method="POST",
        payload={
            "patient_id": patient_id,
            "starts_at": appointment_start.isoformat(timespec="minutes"),
            "reason": "Windows runtime smoke test",
            "notes": "Automated persistence check",
        },
    )
    appointment_id = int(appointment["id"])

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({
        "username": username,
        "password": changed_password,
        "patient_id": patient_id,
        "appointment_id": appointment_id,
        "national_code": national_code,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"FIRST RUN OK: forced password change, dashboard, patient #{patient_id}, appointment #{appointment_id}.")


def verify_records() -> None:
    if not STATE_FILE.is_file():
        raise RuntimeError("Smoke state file is missing; first-run smoke did not complete.")
    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    client = RuntimeClient()
    client.login(state["username"], state["password"], first_login=False)

    patients = client.json_request("/patients/")
    patient = next((row for row in patients if int(row["id"]) == int(state["patient_id"])), None)
    if patient is None or patient.get("national_code") != state["national_code"]:
        raise RuntimeError("Patient record did not survive server restart.")

    appointments = client.json_request("/appointments/")
    appointment = next((row for row in appointments if int(row["id"]) == int(state["appointment_id"])), None)
    if appointment is None or int(appointment["patient_id"]) != int(state["patient_id"]):
        raise RuntimeError("Appointment record did not survive server restart.")

    status, _, dashboard = client.request("/dashboard")
    if status != 200:
        raise RuntimeError(f"Dashboard failed after restart: HTTP {status}.")
    print(f"RESTART OK: admin login, patient #{state['patient_id']} and appointment #{state['appointment_id']} persisted.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("create", "verify"))
    args = parser.parse_args()
    try:
        if args.mode == "create":
            create_records()
        else:
            verify_records()
    except Exception as error:
        print(f"WINDOWS SMOKE FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
