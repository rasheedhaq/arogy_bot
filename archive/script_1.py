# Now let's create the README with setup instructions

readme_content = '''# Arogyamitra - AI Medical Triage Telegram Bot

An intelligent Telegram bot that helps users find appropriate doctors in Kerala based on their symptoms through conversational AI.

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

Create a `.env` file (copy from `.env.example`):

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
ENVIRONMENT=development
```

**Getting your API keys:**

1. **Telegram Bot Token:**
   - Open Telegram and search for @BotFather
   - Send `/newbot` and follow instructions
   - Copy the token provided

2. **Groq API Key:**
   - Visit https://console.groq.com
   - Sign up/login
   - Go to API Keys section
   - Create new key and copy it

### 4. Prepare Data

Ensure your `data/doctors_clean.csv` file is in place with the structure:
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
├── .env.example           # Template for environment variables
├── requirements.txt       # Python dependencies
├── config.py             # Configuration and constants
├── main.py               # Bot entry point
├── bot.py                # Telegram handlers and conversation flow
├── llm_client.py         # Groq API integration
├── doctor_matcher.py     # Doctor matching logic
├── data/
│   └── doctors_clean.csv # Doctor database
└── README.md             # This file
```

## How It Works

1. **User starts conversation** with `/start`
2. **User describes symptoms** in natural language
3. **Bot asks 2-3 clarifying questions** using Groq LLM
4. **Bot collects age and location** for better matching
5. **LLM analyzes conversation** and extracts:
   - Symptoms
   - Severity level
   - Recommended specialty
   - Emergency indicators
6. **Doctor matcher finds** best matches based on:
   - Specialty
   - Symptom keywords
   - Location
   - Availability
7. **Bot presents 1-3 doctors** with:
   - Full details
   - Available slots
   - Contact information

## Safety Features

- ⚠️ Emergency keyword detection (chest pain, breathing issues, etc.)
- 📋 Medical disclaimers on every interaction
- 🚨 Automatic emergency service redirection
- 🔒 No personal health data stored permanently

## Model Choice

**Using Mixtral-8x7b-32768 via Groq:**
- High intelligence for medical triage
- Fast response times (critical for chat)
- Large context window (32K tokens)
- Free tier available for MVP testing
- Falls back gracefully on API errors

## API Costs (Groq Free Tier)

Groq offers generous free tier limits:
- ~14,400 requests/day for Mixtral
- Perfect for MVP testing
- Upgrade to paid tier only when needed

## Development Tips

### Local Testing
```bash
# Run with debug output
python main.py
```

### Reset User Session
User sessions are stored in memory. Restart the bot to clear all sessions.

### Add More Doctors
Simply add rows to `data/doctors_clean.csv` following the schema.

### Customize Questions
Edit the prompts in `llm_client.py` to adjust:
- Question style
- Number of clarifications
- Triage logic

### Deploy to Production

**Option 1: Railway (Recommended)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and init
railway login
railway init

# Add environment variables in Railway dashboard
# Deploy
railway up
```

**Option 2: Render/Heroku/PythonAnywhere**
- Set environment variables in platform dashboard
- Ensure Python 3.9+ runtime
- Deploy via Git push

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

## Future Enhancements

- [ ] Google Meet booking integration
- [ ] WhatsApp channel support
- [ ] Multi-language support (Malayalam, Hindi)
- [ ] Image upload for skin conditions
- [ ] Prescription OCR
- [ ] Follow-up reminders
- [ ] Doctor review system

## Contributing

This is an MVP. Suggestions and improvements welcome!

## License

MIT License - Free for educational and non-commercial use.

## Disclaimer

This bot is for informational purposes only. It does not provide medical diagnosis or treatment. Always consult qualified healthcare professionals for medical advice.

## Contact

For issues or questions, contact the development team.

---

Built with ❤️ for better healthcare access in Kerala
'''

print("=== README.md ===")
print(readme_content)
print("\n" + "="*60)
print("✅ All files ready!")
print("="*60)

# Archived script_1.py
# Moved to archive for workspace minimalism.
