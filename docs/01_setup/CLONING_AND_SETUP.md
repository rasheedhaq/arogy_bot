# Cloning & Setup — Arogyamitra Bot

Purpose
-------
This document explains everything a new developer needs to do to clone, configure, and run the project locally or deploy to Railway. The repository intentionally keeps sensitive credentials out of source; you must create provider accounts and populate a local `.env` before the bot will work.

Important: do NOT commit your `.env` or API keys. `rate_limits.json` and other runtime files are gitignored.

Prerequisites
-------------
- Git installed and configured
- PowerShell (Windows) or bash (Linux/macOS)
- Python 3.10+ (recommended 3.11 or 3.12 compatible with project) and pip
- Conda (optional) or virtualenv for environment isolation
- A Telegram account to create a bot token via BotFather
- Accounts/API keys for at least one LLM provider you intend to test (Groq/OpenRouter/Gemini/HuggingFace/Deepseek)

Accounts & Keys to create
-------------------------
You don't need all providers — a single working provider is enough to test, but the project supports multiple fallbacks.

1. Telegram Bot (BotFather)
   - Create a bot using BotFather on Telegram and copy the `TELEGRAM_BOT_TOKEN`.

2. Groq (optional primary)
   - Sign up and get `GROQ_API_KEY` if you plan to use Groq as the main LLM.

3. Google Gemini / Google Generative AI (optional)
   - If using Gemini via `google-generativeai`, obtain `GEMINI_API_KEY` and prefer package version pinned in `requirements.txt`.
   - Note: `google-generativeai==0.7.2` is recommended on some platforms to avoid Windows metadata issues.

4. OpenRouter (optional fallback)
   - Create an account and get `OPENROUTER_API_KEY`. Set `OPENROUTER_MODEL` in config if needed.

5. HuggingFace (optional)
   - Create `HUGGINGFACE_API_KEY` and ensure compatible model names if you use HF endpoints.

6. Deepseek / Together / Anthropic (optional)
   - Add `DEEPSEEK_API_KEY`, `TOGETHER_API_KEY`, `ANTHROPIC_API_KEY` if you want to test these providers.

Project files you should be aware of
-----------------------------------
- `.env.example` — template of environment variables. Copy to `.env` and update values.
- `requirements.txt` — Python dependencies
- `data/` — contains `doctors_clean.csv` and `doctors_enhanced.csv` (sample doctor data)
- `docs/01_setup/` — setup docs (this file lives here)
- `rate_limits.json` — runtime file (gitignored)

Step-by-step local setup (PowerShell)
------------------------------------
1. Clone repository

```powershell
git clone https://github.com/rasheedhaq/arogy_bot.git
cd arogy_bot
```

2. Create and activate environment (Conda example)

```powershell
conda create -n arogyamitra_env python=3.11 -y
conda activate arogyamitra_env
```

Or virtualenv (native):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and fill in keys

```powershell
copy .env.example .env
# then edit .env in an editor and add tokens
notepad .env
```

Required `.env` variables (minimum to run):
- TELEGRAM_BOT_TOKEN=your_telegram_token_here
- DOCTORS_DB_PATH=data/doctors_clean.csv
- At least one LLM provider key (e.g., GROQ_API_KEY or OPENROUTER_API_KEY or GEMINI_API_KEY)

Optional environment variables you may want to set:
- USE_GEMINI=true/false (set to false on Windows if you encounter package/metadata issues)
- HUGGINGFACE_API_KEY=...
- DEEPSEEK_API_KEY=...
- OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free

5. Run the bot locally

```powershell
conda activate arogyamitra_env   # or activate your venv
python main.py
```

You should see startup logs like "LLM Providers initialized" and "Loaded X doctors from database".

Windows-specific notes
----------------------
- There is a known `google-generativeai` metadata import issue on some Windows setups; if you hit an import error, set `USE_GEMINI=false` in your `.env` or use Linux (WSL) / Railway for deployment.
- If the bot fails with `AsyncLibraryNotFoundError` when running `python main.py`, ensure `python-telegram-bot==22.5` is installed and run inside the activated environment.

Testing the multi-field extraction flow
--------------------------------------
- Start the bot locally and open the Telegram bot.
- Type `/start` to begin. The bot should ask for name first.
- Reply with multiple fields in one message (e.g., `Rasheed male 33 9876543210, Palakkad`).
- The bot should extract name, sex, age, mobile, and address where present and skip asking already-collected questions.

Troubleshooting / quick checks
-----------------------------
- No providers initialized? Check your `.env` keys and `requirements.txt` installed.
- If rate limits occur, the bot will write to `rate_limits.json` and skip providers for 24 hours. This file is gitignored.
- If the bot restarts and re-asks for fields it already had, verify `context.user_data` is initialized correctly; conversation persistence across restarts is not implemented by default (planned for enhanced versions).

Deploying to Railway
--------------------
- Create a Railway project and connect your GitHub repo.
- Add environment variables in Railway's dashboard (same keys you used in `.env`). Do NOT commit `.env` to the repo.
- Use the `Procfile` (already present) and ensure `runtime.txt` and `requirements.txt` match Python version and libs.

Security & privacy guidance
---------------------------
- Never commit `.env` or `rate_limits.json` or any private keys. They are listed in `.gitignore`.
- If you share the repo, make sure to keep it private on GitHub or selectively remove sensitive data.
- For production, consider storing secrets in Railway's environment secrets or a secrets manager.

Final checklist for a new developer
----------------------------------
- [ ] Clone repo
- [ ] Create environment and install deps
- [ ] Create `.env` from `.env.example` and add at least one LLM key + Telegram bot token
- [ ] Run `python main.py` and verify provider init and doctors loaded
- [ ] Test `/start` and multi-field extraction
- [ ] If deploying, add env vars to Railway and set branch to `1_MVP_base` or `dev` depending on stability

If you want, I can also generate a short script to validate environment variables are present and show helpful error messages if keys are missing — would you like that added to the repo?