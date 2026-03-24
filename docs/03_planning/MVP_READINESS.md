# MVP Readiness

**Last Updated:** March 24, 2026  
**Status:** Active

## Current Active Build

The launchable codebase is `arogy_bot`, not the older sibling folders in the wider `DSHAFQ` workspace.

What is already implemented:

- Telegram bot entrypoint in `main.py`
- Natural consultation flow in `app/bot_intelligent.py`
- Multi-provider free-tier LLM fallback in `app/llm_client.py`
- Doctor matching against CSV data in `app/doctor_matcher.py`
- Local SQLite storage for user and consultation logs in `app/database.py`
- Unit tests under `tests/`
- Organized documentation under `docs/`

What is archival or experimental:

- `test_scripts/` contains older ad-hoc experiments and should not be treated as the supported test suite
- Sibling folders like `arogyamithra`, `arogyamitra_bot`, and `idea_1_arogyamitra` are reference/history, not the launch target

## Free MVP Launch Shape

The lowest-cost MVP should stay intentionally narrow:

- Channel: Telegram only
- Hosting: local machine, Railway free tier, or Render free tier
- Storage: CSV + SQLite only
- LLM: free-tier provider only, with Groq or Gemini/OpenRouter free models preferred
- Scope: symptom intake, specialty recommendation, doctor suggestions, disclaimer

This keeps the MVP free while avoiding feature work that would force paid APIs:

- No Google Maps dependency
- No paid WhatsApp Business launch path
- No booking or payments in MVP0
- No managed database required for initial release

## Launch Blockers To Clear

1. Finalize a single supported `.env` using only free-tier providers.
2. Refresh the doctor data through `scripts/update_doctors_db.py`.
3. Run `pytest` from the repo root and keep `tests/` green.
4. Perform one end-to-end Telegram conversation test with real API keys.
5. Decide whether production will run by polling or webhook before deployment.

## Suggested Launch Sequence

1. Update `data/doctors_enhanced.csv` with real doctor records.
2. Run `python scripts/update_doctors_db.py`.
3. Copy `.env.example` to `.env` and keep only free-tier API keys enabled.
4. Run `pytest`.
5. Run `python main.py`.
6. Test scenarios:
   - tooth pain -> Dentist
   - chest pain -> emergency warning / safe handling
   - fever -> General Physician
7. Deploy only after local verification passes.
