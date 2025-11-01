# Arogyamitra - AI Medical Triage Telegram Bot

**Objective:**
Arogyamitra is an intelligent Telegram bot designed to help users in Kerala find the most suitable doctors based on their symptoms. It uses conversational AI to collect symptoms, clarify details, and match users to doctors from a curated database, supporting online consultations and emergency detection.

## Features

- 🤖 GPT-level conversational intelligence using Groq API
- 💬 Natural language symptom collection (2-3 clarifying questions)
- 🎯 Smart doctor matching based on symptoms and specialty
- 📅 Real-time availability and slot information
- 💻 Online consultation support
- ⚠️ Emergency detection and safety disclaimers
- 🏥 Curated Kerala doctor database

## Quick Setup

### 1. Prerequisites

- Python 3.9 or higher
- Telegram Bot Token (from @BotFather)
- Groq API Key (from https://console.groq.com)

### 2. Installation

```bash
# Clone or create project directory
mkdir arogyamitra
cd arogyamitra

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory:

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
ENVIRONMENT=development
```

**Getting your API keys:**

**Telegram Bot Token:**
- Open Telegram and search for @BotFather
- Send `/newbot` and follow instructions
- Copy the token provided

**Groq API Key:**
- Visit https://console.groq.com
- Sign up/login (free account)
- Go to API Keys section
- Create new key and copy it

### 4. Prepare Data

Create a `data` folder and add your `doctors_clean.csv` file with the structure:
```
Doctor_Name,Specialty,Clinic_Name,Address,Locality,Lat,Lon,Keywords,Email,OnlineConsult,SlotsISO,SlotDurationMin
```

### 5. Run the Bot

```bash
python main.py
```

You should see:
```
Starting Arogyamitra Bot...
Loaded X doctors from database
Bot is running. Press Ctrl+C to stop.
```

### 6. Test on Telegram

1. Open Telegram and search for your bot (username you set with BotFather)
2. Send `/start`
3. Describe your symptoms
4. Follow the conversation

## Project Structure

```
arogyamitra/
├── .env                    # Your environment variables (DO NOT COMMIT)
├── requirements.txt        # Python dependencies
├── config.py              # Configuration and constants
├── main.py                # Bot entry point
├── bot.py                 # Telegram handlers and conversation flow
├── llm_client.py          # Groq API integration
├── doctor_matcher.py      # Doctor matching logic
├── data/
│   └── doctors_clean.csv  # Doctor database
└── README.md              # This file
```

## How It Works

1. User starts conversation with `/start`
2. User describes symptoms in natural language
3. Bot asks 2-3 clarifying questions using Groq LLM
4. Bot collects age and location for better matching
5. LLM analyzes conversation and extracts:
   - Symptoms
   - Severity level
   - Recommended specialty
   - Emergency indicators
6. Doctor matcher finds best matches based on:
   - Specialty
   - Symptom keywords
   - Availability
7. Bot presents 1-3 doctors with:
   - Full details
   - Available slots
   - Contact information

## Code Flow Overview

- `main.py`: Entry point. Starts the bot and loads configuration/data.
- `bot.py`: Handles Telegram messaging, user interaction, and conversation logic.
- `llm_client.py`: Connects to Groq API for natural language understanding and clarifying questions.
- `doctor_matcher.py`: Matches user symptoms to doctors using the database and extracted keywords.
- `config.py`: Stores configuration, constants, and file paths.
- `data/doctors_clean.csv`: Doctor database used for matching.

**Typical Flow:**
1. User sends `/start` to the bot.
2. Bot collects symptoms and clarifies details using LLM.
3. Extracted info is passed to `doctor_matcher.py` to find suitable doctors.
4. Bot presents doctor options and available slots to the user.
5. Emergency cases are detected and redirected as needed.

## Safety Features

- Emergency keyword detection (chest pain, breathing issues, etc.)
- Medical disclaimers on every interaction
- Automatic emergency service redirection
- No personal health data stored permanently

## Model Choice

**Using Mixtral-8x7b-32768 via Groq:**
- High intelligence for medical triage
- Fast response times (critical for chat)
- Large context window (32K tokens)
- Free tier available for MVP testing

## Troubleshooting

### Bot not responding
- Check your bot token is correct
- Verify bot is running (`python main.py`)
- Check Telegram bot privacy settings with @BotFather

### "Error calling Groq API"
- Verify GROQ_API_KEY in .env
- Check API quota at console.groq.com
- Verify internet connection

### No doctors found
- Check CSV file path in config.py
- Verify CSV formatting
- Ensure keywords match symptom descriptions

### Import errors
```bash
pip install --upgrade -r requirements.txt
```

## Deployment

**For Production (Railway/Render):**
1. Set environment variables in platform dashboard
2. Ensure Python 3.9+ runtime
3. Deploy via Git push

## License

MIT License - Free for educational and non-commercial use.

## Disclaimer

This bot is for informational purposes only. It does not provide medical diagnosis or treatment. Always consult qualified healthcare professionals for medical advice.

---

Built with ❤️ for better healthcare access in Kerala