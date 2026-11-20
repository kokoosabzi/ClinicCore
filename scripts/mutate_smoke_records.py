"""Mutate smoke records after backup so Windows CI can prove restore works."""
import json
import os
import sqlite3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
state_path = root / "data" / "windows-smoke-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
database_url = os.environ.get("DATABASE_URL", "sqlite:///./data/cliniccore.db")
if not database_url.startswith("sqlite:///"):
    raise SystemExit("A file-backed SQLite database is required.")
database_path = Path(database_url[len("sqlite:///"):])
if not database_path.is_absolute():
    database_path = root / database_path
with sqlite3.connect(database_path) as connection:
    patient = connection.execute("UPDATE patients SET national_code = ? WHERE id = ?", ("0000000000", state["patient_id"]))
    appointment = connection.execute("UPDATE appointments SET reason = ? WHERE id = ?", ("mutated after backup", state["appointment_id"]))
    if patient.rowcount != 1 or appointment.rowcount != 1:
        raise SystemExit("Could not mutate both smoke records after backup.")
    connection.commit()
print("POST-BACKUP MUTATION OK: patient and appointment changed while ClinicCore was stopped.")