# Database Pipeline

**Last Updated:** March 24, 2026  
**Status:** Active

## Goal

Keep doctor data up to date for the MVP without paying for external ETL, managed databases, or admin tools.

## Source Of Truth

Use `data/doctors_enhanced.csv` as the canonical doctor dataset.

This file should be maintained manually or exported from your data collection sheet, then normalized through the local pipeline script.

## Pipeline Outputs

Run:

```powershell
python scripts/update_doctors_db.py
```

This generates and refreshes:

- `data/doctors_enhanced.csv`
  Normalized canonical dataset
- `data/doctors_clean.csv`
  Legacy matcher-compatible flattened file
- `data/doctors_sample.csv`
  Safe sample dataset for sharing or demos
- `data/arogy.db`
  SQLite snapshot with a `doctors` table
- `data/pipeline_report.json`
  Summary of row counts and generated outputs

## Recommended Update Workflow

1. Edit or replace `data/doctors_enhanced.csv`.
2. Run `python scripts/update_doctors_db.py`.
3. Review `data/pipeline_report.json`.
4. Run `pytest`.
5. Start the bot and test at least one specialty flow manually.

## Minimum Required Columns

- `doctor_id`
- `full_name`
- `specialty`
- `primary_symptoms`
- `clinic_name`
- `address`
- `pincode`
- `city`
- `phone_number`
- `online_consult_available`
- `appointment_required`

## Why This Works For A Free MVP

- No paid database is needed
- SQLite is enough for local state and sync snapshots
- CSV remains easy to edit by non-developers
- The script gives one repeatable command for refreshing launch data

## Future Upgrade Path

When the MVP starts getting regular usage, the same pipeline can later publish into:

- Supabase free tier
- PostgreSQL on Railway/Render
- Google Sheets export + scheduled sync

For MVP0, keep the pipeline local and simple.
