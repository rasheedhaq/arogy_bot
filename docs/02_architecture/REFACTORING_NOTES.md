# Configuration Refactoring Complete ✅

## What Changed:

### 1. **New `config.yml` file**
All bot messages, settings, and prompts are now in a centralized YAML file for easy editing:
- Bot messages (welcome, emergency, disclaimers)
- Conversation settings (max questions, max results)
- Emergency keywords
- AI prompts (triage, clarifying questions)
- API settings (temperature, tokens)

### 2. **Updated `config.py`**
Now loads from YAML and allows environment variable overrides:
- Reads config.yml on startup
- Environment variables take precedence
- Cleaner, more organized structure

### 3. **Updated `bot.py`**
- Uses config constants instead of hardcoded strings
- Easier to maintain and translate

### 4. **Updated `llm_client.py`**
- Uses config for prompts and API settings
- More flexible and configurable

### 5. **Updated `requirements.txt`**
- Added `pyyaml>=6.0` for YAML support

## Benefits:

✅ **Easy to customize**: Edit messages in config.yml without touching code
✅ **Translatable**: Can create config_ml.yml for Malayalam, etc.
✅ **Maintainable**: All settings in one place
✅ **Flexible**: Override with environment variables when needed
✅ **Clean code**: No hardcoded strings in business logic

## Current Settings:

```yaml
max_clarifying_questions: 1
max_doctor_results: 2
```

## To Run:

```bash
conda activate arogyamitra_env
python main.py
```

The bot will now show only 2 doctors and ask only 1 clarifying question by default.
