"""Regression tests for fresh file-backed SQLite installations."""

import os
import sqlite3
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_alembic_migrations_create_file_backed_sqlite_schema(tmp_path: Path) -> None:
    database_path = tmp_path / "nested" / "cliniccore.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{database_path.as_posix()}"

    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert database_path.is_file()

    with sqlite3.connect(database_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert {
            "alembic_version",
            "patients",
            "appointments",
            "users",
            "payments",
            "expenses",
            "messages",
            "audit_logs",
            "system_settings",
        }.issubset(tables)

        indexes = {
            row[1]
            for row in connection.execute("PRAGMA index_list('appointments')")
        }
        assert "uq_active_appointment_starts_at" in indexes

        version = connection.execute(
            "SELECT version_num FROM alembic_version"
        ).fetchone()
        assert version == ("20261005_0005",)
