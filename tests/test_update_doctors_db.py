import sqlite3
from pathlib import Path

import pandas as pd

from scripts.update_doctors_db import normalize_dataframe, sync_sqlite


def test_sync_sqlite_records_source_file(tmp_path):
    source_path = tmp_path / "doctors.csv"
    db_path = tmp_path / "arogy.db"

    frame = pd.DataFrame(
        [
            {
                "doctor_id": "DOC_001",
                "full_name": "Dr. Test",
                "specialty": "Dentist",
                "primary_symptoms": "tooth_pain",
                "clinic_name": "Test Clinic",
                "address": "123 Test Street",
                "pincode": "679000",
                "city": "Test City",
                "phone_number": "9999999999",
                "online_consult_available": "true",
                "appointment_required": "true",
            }
        ]
    )

    normalized = normalize_dataframe(frame)
    sync_sqlite(normalized, db_path, source_path)

    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            "SELECT source_file, row_count FROM pipeline_runs ORDER BY id DESC LIMIT 1"
        ).fetchone()

    assert row == (str(source_path), 1)
