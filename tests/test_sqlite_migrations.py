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
            "roles",
            "permissions",
            "role_permissions",
        }.issubset(tables)

        indexes = {
            row[1]
            for row in connection.execute("PRAGMA index_list('appointments')")
        }
        assert "uq_active_appointment_starts_at" in indexes

        version = connection.execute(
            "SELECT version_num FROM alembic_version"
        ).fetchone()
        assert version == ("20261106_0006",)


def test_rbac_migration_preserves_existing_users_and_password_hashes(tmp_path: Path) -> None:
    database_path = tmp_path / "existing" / "cliniccore.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{database_path.as_posix()}"

    baseline = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "20261005_0005"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert baseline.returncode == 0, baseline.stdout + "\n" + baseline.stderr

    original_hash = "existing-password-hash-must-remain-unchanged"
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            INSERT INTO users
                (full_name, username, password_hash, role, must_change_password, is_deleted)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("Existing Admin", "existing.admin", original_hash, "admin", 0, 0),
        )
        connection.commit()

    upgraded = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert upgraded.returncode == 0, upgraded.stdout + "\n" + upgraded.stderr

    with sqlite3.connect(database_path) as connection:
        user = connection.execute(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            ("existing.admin",),
        ).fetchone()
        assert user == ("existing.admin", original_hash, "admin")

        role_count = connection.execute(
            "SELECT COUNT(*) FROM roles"
        ).fetchone()[0]
        admin_grant_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM role_permissions rp
            JOIN roles r ON r.id = rp.role_id
            WHERE r.key = 'admin'
            """
        ).fetchone()[0]
        assert role_count == 5
        assert admin_grant_count > 0
