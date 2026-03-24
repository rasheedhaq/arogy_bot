"""
Normalize doctor CSV data, generate derived files, and sync the local SQLite DB.

This keeps the MVP's doctor search data reproducible without introducing any paid
services or external infrastructure.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Iterable

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT_DIR / "data" / "doctors_enhanced.csv"
DEFAULT_LEGACY_OUTPUT = ROOT_DIR / "data" / "doctors_clean.csv"
DEFAULT_SAMPLE_OUTPUT = ROOT_DIR / "data" / "doctors_sample.csv"
DEFAULT_SQLITE_DB = ROOT_DIR / "data" / "arogy.db"
DEFAULT_REPORT = ROOT_DIR / "data" / "pipeline_report.json"

REQUIRED_COLUMNS = [
    "doctor_id",
    "full_name",
    "specialty",
    "primary_symptoms",
    "clinic_name",
    "address",
    "pincode",
    "city",
    "phone_number",
    "online_consult_available",
    "appointment_required",
]

TEXT_COLUMNS = [
    "doctor_id",
    "full_name",
    "specialty",
    "sub_specialty",
    "qualification",
    "primary_symptoms",
    "secondary_symptoms",
    "exclude_keywords",
    "age_groups_treated",
    "clinic_name",
    "address",
    "city",
    "phone_number",
    "whatsapp_number",
    "email",
    "consultation_days",
    "consultation_hours_start",
    "consultation_hours_end",
    "insurance_accepted",
    "diagnostic_services",
    "procedures_offered",
    "languages_spoken",
]

BOOLEAN_COLUMNS = [
    "emergency_capable",
    "online_consult_available",
    "appointment_required",
    "wheelchair_accessible",
]

INTEGER_COLUMNS = [
    "experience_years",
    "average_wait_time_mins",
    "consultation_fee",
    "online_fee",
]

LIST_COLUMNS = [
    "primary_symptoms",
    "secondary_symptoms",
    "exclude_keywords",
    "consultation_days",
    "insurance_accepted",
    "diagnostic_services",
    "procedures_offered",
    "languages_spoken",
]


def normalize_text(value: object) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return " ".join(str(value).strip().split())


def normalize_list(value: object) -> str:
    raw = normalize_text(value)
    if not raw:
        return ""

    normalized = raw.replace(";", ",")
    parts = []
    seen = set()
    for part in normalized.split(","):
        item = normalize_text(part)
        if not item:
            continue
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        parts.append(item)
    return ",".join(parts)


def normalize_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value

    text = normalize_text(value).lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n", ""}:
        return False
    raise ValueError(f"Unsupported boolean value: {value!r}")


def normalize_int(value: object) -> int:
    text = normalize_text(value)
    if not text:
        return 0
    return int(float(text))


def ensure_required_columns(frame: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def normalize_dataframe(frame: pd.DataFrame) -> pd.DataFrame:
    ensure_required_columns(frame)
    normalized = frame.copy()

    for column in TEXT_COLUMNS:
        if column in normalized.columns:
            normalized[column] = normalized[column].apply(normalize_text)

    for column in LIST_COLUMNS:
        if column in normalized.columns:
            normalized[column] = normalized[column].apply(normalize_list)

    for column in BOOLEAN_COLUMNS:
        if column in normalized.columns:
            normalized[column] = normalized[column].apply(normalize_bool)

    for column in INTEGER_COLUMNS:
        if column in normalized.columns:
            normalized[column] = normalized[column].apply(normalize_int)

    normalized = normalized.drop_duplicates(subset=["doctor_id"], keep="last")
    normalized = normalized.drop_duplicates(subset=["full_name", "clinic_name"], keep="last")
    normalized = normalized.sort_values(
        by=["city", "specialty", "full_name"],
        na_position="last",
    ).reset_index(drop=True)

    return normalized


def build_legacy_matcher_csv(frame: pd.DataFrame) -> pd.DataFrame:
    keywords = []
    for _, row in frame.iterrows():
        combined = normalize_list(
            ",".join(
                filter(
                    None,
                    [
                        normalize_text(row.get("primary_symptoms", "")),
                        normalize_text(row.get("secondary_symptoms", "")),
                    ],
                )
            )
        )
        keywords.append(combined)

    return pd.DataFrame(
        {
            "Doctor_Name": frame.get("full_name", ""),
            "Specialty": frame.get("specialty", ""),
            "Clinic_Name": frame.get("clinic_name", ""),
            "Address": frame.get("address", ""),
            "Pincode": frame.get("pincode", ""),
            "Keywords": keywords,
        }
    )


def build_public_sample(frame: pd.DataFrame, size: int = 5) -> pd.DataFrame:
    sample = frame.head(size).copy()
    if sample.empty:
        return sample

    if "pincode" in sample.columns:
        sample["pincode"] = sample["pincode"].astype(str)

    for index, row in sample.iterrows():
        sample.at[index, "doctor_id"] = f"DOC_SAMPLE_{index + 1:03d}"
        sample.at[index, "full_name"] = f"Dr. Sample {row.get('specialty', 'Doctor')}"
        sample.at[index, "phone_number"] = f"90000000{index:02d}"
        sample.at[index, "whatsapp_number"] = f"90000000{index:02d}"
        sample.at[index, "email"] = f"sample{index + 1}@example.com"
        sample.at[index, "address"] = f"{index + 1} Sample Street"
        sample.at[index, "pincode"] = "000000"
        sample.at[index, "city"] = "Sample City"
        if "latitude" in sample.columns:
            sample.at[index, "latitude"] = 0.0
        if "longitude" in sample.columns:
            sample.at[index, "longitude"] = 0.0
    return sample


def sync_sqlite(frame: pd.DataFrame, db_path: Path, source_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        frame.to_sql("doctors", connection, if_exists="replace", index=False)
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file TEXT NOT NULL,
                row_count INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            "INSERT INTO pipeline_runs (source_file, row_count) VALUES (?, ?)",
            (str(source_path), len(frame)),
        )
        connection.commit()


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def generate_report(frame: pd.DataFrame, outputs: Iterable[Path]) -> dict:
    return {
        "doctor_count": int(len(frame)),
        "specialty_count": int(frame["specialty"].nunique()) if "specialty" in frame.columns else 0,
        "city_count": int(frame["city"].nunique()) if "city" in frame.columns else 0,
        "online_consult_count": int(frame["online_consult_available"].sum()) if "online_consult_available" in frame.columns else 0,
        "outputs": [str(path) for path in outputs],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh the Arogyamitra doctor database assets.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Canonical doctor CSV input.")
    parser.add_argument("--legacy-output", type=Path, default=DEFAULT_LEGACY_OUTPUT, help="Legacy matcher CSV output.")
    parser.add_argument("--sample-output", type=Path, default=DEFAULT_SAMPLE_OUTPUT, help="Public sample CSV output.")
    parser.add_argument("--sqlite-db", type=Path, default=DEFAULT_SQLITE_DB, help="SQLite DB to sync.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="JSON summary report output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()

    frame = pd.read_csv(source)
    normalized = normalize_dataframe(frame)

    write_csv(normalized, source)
    write_csv(build_legacy_matcher_csv(normalized), args.legacy_output)
    write_csv(build_public_sample(normalized), args.sample_output)
    sync_sqlite(normalized, args.sqlite_db, source)

    report = generate_report(
        normalized,
        [source, args.legacy_output.resolve(), args.sample_output.resolve(), args.sqlite_db.resolve()],
    )
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
