# 🏥 Arogyamitra Medical Bot - ARM_MVP0

**Zero-cost AI-powered medical triage chatbot for Telegram**

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Groq](https://img.shields.io/badge/AI-Groq%20LLama%203.3-green.svg)](https://groq.com/)

## 🎯 What is ARM_MVP0?

Arogyamitra (आरोग्यमित्र - "Health Friend" in Sanskrit) is an intelligent medical assistant bot that:
- ✅ Asks structured 8-question medical history (SOAP protocol)
- ✅ Uses AI (Groq LLama 3.3) to analyze symptoms
- ✅ Matches patients to appropriate doctors based on specialty
- ✅ 100% FREE to run (using free-tier APIs)
- ✅ Prevents mismatches with smart exclude_keywords algorithm

**MVP0 = Zero Cost:** Designed to run entirely on free services!

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Telegram account
- Groq API key (free)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/arogy_bot.git
cd arogy_bot
```

2. **Create virtual environment**
```bash
conda create -n arogyamitra_env python=3.13
conda activate arogyamitra_env
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys:
# - TELEGRAM_BOT_TOKEN (from @BotFather)
# - GROQ_API_KEY (from https://console.groq.com)
```

5. **Prepare doctor database**
```bash
# Copy sample data or add your own doctors
cp data/doctors_sample.csv data/doctors_enhanced.csv
# Edit doctors_enhanced.csv with real doctor data
```

6. **Run the bot**
```bash
python main.py
```

---

## 📊 Architecture

```
User (Telegram) → Bot (8 Questions) → LLM (Groq) → Doctor Matcher → Results
```

### Key Components:
- **`main.py`**: Entry point, starts the bot
- **`bot.py`**: Telegram conversation handler (8-question flow)
- **`llm_client.py`**: Groq API integration for symptom analysis
- **`doctor_matcher.py`**: 5-step matching algorithm with exclude_keywords
- **`config.yml`**: All messages and prompts
- **`config.py`**: Settings loader

---

## 🔒 Security Features

### What's Protected:
- ✅ API keys in `.env` (never committed)
- ✅ Real doctor data excluded from git
- ✅ Sample data provided for testing
- ✅ `.gitignore` configured properly

### Data disclaimer
All records in `data/doctors_enhanced.csv` are synthetic or publicly sourced sample data for testing and do not contain real personal patient information.

### Before Deployment:
1. Never commit `.env` file
2. Use environment variables on hosting platform
3. Keep doctor data private (GDPR compliance)

---

## 💡 How It Works

### 8-Question Medical Protocol
1. **Chief Complaint**: Main problem (e.g., "tooth pain")
2. **Duration**: How long (e.g., "2 days")
3. **Severity**: Mild/Moderate/Severe
4. **Associated Symptoms**: Other symptoms
5. **Age**: Patient age
6. **Location**: Where is the pain/issue
7. **Chronic Conditions**: Existing conditions
8. **Medications**: Current medications

### Doctor Matching Algorithm (5 Steps)
```python
Step 1: EXCLUDE - Check exclude_keywords (prevents tooth→oncologist)
Step 2: SPECIALTY - Match specialty (weight: 20)
Step 3: PRIMARY - Match primary_symptoms (weight: 10)
Step 4: SECONDARY - Match secondary_symptoms (weight: 5)
Step 5: KEYWORDS - Fallback keyword match (weight: 3)
```

**Example:**
- Input: "tooth pain"
- Excluded: Medical Oncologist (exclude_keywords: "tooth,dental")
- Matched: Dentist (primary_symptoms: "tooth_pain,cavity")
- Result: ✅ Dentist recommended (NOT Oncologist)

---

## 📁 Project Structure

```
arogy_bot/
├── main.py                 # Bot entry point
├── bot.py                  # Telegram handlers
├── llm_client.py           # Groq AI integration
├── doctor_matcher.py       # Matching algorithm
├── config.py               # Configuration loader
├── config.yml              # Messages & prompts
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git exclusions
├── README.md               # This file
├── data/
│   ├── doctors_sample.csv  # Sample data (committed)
│   └── doctors_enhanced.csv # Real data (excluded)
└── docs/                   # Documentation
    ├── DATA_SCHEMA.md
    ├── DATA_COLLECTION_TEMPLATE.md
    ├── FULL_PLATFORM_ROADMAP.md
    ├── IMPLEMENTATION_SUMMARY.md
    ├── ISSUE_ANALYSIS.md
    └── VISUAL_ARCHITECTURE.md
```

---

## 🌐 Free Hosting Options

### Option 1: Railway.app (Recommended)
- ✅ 500 hours/month free
- ✅ Auto-deploy from GitHub
- ✅ Environment variables support

### Option 2: Render.com
- ✅ Free tier available
- ✅ Auto-sleep after inactivity
- ✅ Easy setup

### Option 3: PythonAnywhere
- ✅ Free tier: 1 web app
- ✅ Always-on for paid ($5/month)

### Option 4: Fly.io
- ✅ Free tier: 3 VMs
- ✅ Good performance

**Deployment guide:** See `docs/DEPLOYMENT.md`

---

## 💰 Cost Analysis

### MVP0 (Current):
- Telegram Bot: **FREE**
- Groq API: **FREE** (14,400 requests/day)
- Hosting: **FREE** (Railway/Render)
- **Total: ₹0/month**

### Future Phases:
- Phase 2 (Availability): ~₹2,500/month
- Phase 3 (Location): ~₹2,500/month
- Phase 4 (Booking): ~₹5,000/month
- Phase 5 (Payment): ~₹10,000/month + 2% transaction fee

---

## 📚 Documentation

- **[Data Schema](docs/DATA_SCHEMA.md)**: Database design (MVP + 6 phases)
- **[Data Collection Template](docs/DATA_COLLECTION_TEMPLATE.md)**: How to add doctors
- **[Full Platform Roadmap](docs/FULL_PLATFORM_ROADMAP.md)**: 6-phase implementation plan
- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)**: Executive overview
- **[Issue Analysis](docs/ISSUE_ANALYSIS.md)**: Oncologist bug fix
- **[Visual Architecture](docs/VISUAL_ARCHITECTURE.md)**: Flow diagrams

---

## 🧪 Testing

### Test the Oncologist Bug Fix:
1. Open Telegram: `@arogyamitr_bot`
2. Send `/start`
3. Answer with: "tooth pain" scenario
4. **Expected:** Dr. Priya Sharma (Dentist) ✅
5. **NOT:** Medical Oncologist ❌

### Sample Test Cases:
- Tooth pain → Dentist
- Chest pain → Cardiologist
- Fever, cold → General Physician
- Joint pain → Orthopedist

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/arogy_bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/arogy_bot/discussions)
- **Email**: your-email@example.com

---

## 🎯 Roadmap

- [x] **MVP0**: Symptom → Doctor matching (FREE)
- [ ] **Phase 1**: Real doctor database (50+ doctors)
- [ ] **Phase 2**: Availability checking
- [ ] **Phase 3**: Location filtering (Google Maps)
- [ ] **Phase 4**: Booking system
- [ ] **Phase 5**: Payment integration (Razorpay)
- [ ] **Phase 6**: Reviews & follow-ups

---

## ⚡ Performance

- Response time: < 5 seconds
- Groq API: ~1-2 seconds
- Doctor matching: < 500ms
- Telegram delivery: ~1 second

---

## 🙏 Acknowledgments

- **Groq** for free LLama 3.3 API
- **Telegram** for Bot API
- **Python Telegram Bot** library
- Open source community

---

**Built with ❤️ for accessible healthcare**

*Version: MVP0 (ARM_MVP0)*
*Last Updated: November 1, 2025*
