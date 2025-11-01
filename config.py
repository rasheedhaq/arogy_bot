
# =====================
# Environment & Loading
# =====================
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

# Load YAML configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
with open(config_path, 'r', encoding='utf-8') as f:
    CONFIG = yaml.safe_load(f)

# =====================
# Bot & API Keys
# =====================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-405b-reasoning")

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").lower() == "true"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# =====================
# Data & Integration
# =====================
DOCTORS_DB_PATH = os.getenv("DOCTORS_DB_PATH", CONFIG['data']['doctors_db'])
# WhatsApp integration (future)
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "verify-me")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")

# =====================
# App Settings
# =====================
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# =====================
# Conversation Settings (from YAML with env override)
# =====================
MAX_CLARIFYING_QUESTIONS = int(os.getenv("MAX_CLARIFYING_QUESTIONS", CONFIG['conversation']['max_clarifying_questions']))
MAX_DOCTOR_RESULTS = int(os.getenv("MAX_DOCTOR_RESULTS", CONFIG['conversation']['max_doctor_results']))
ENABLE_AUTO_RESPONSE = os.getenv("ENABLE_AUTO_RESPONSE", str(CONFIG['conversation']['enable_auto_response'])).lower() == "true"

# =====================
# Emergency Keywords (from YAML)
# =====================
EMERGENCY_KEYWORDS = set(CONFIG['emergency']['keywords'])

# =====================
# Bot Messages (from YAML)
# =====================
EMERGENCY_MESSAGE = CONFIG['messages']['emergency']
GENERAL_DISCLAIMER = CONFIG['messages']['disclaimer']
WELCOME_MESSAGE = CONFIG['messages']['welcome']
EMERGENCY_DETECTED_MESSAGE = CONFIG['messages']['emergency_detected']
COLLECTING_INFO_MESSAGE = CONFIG['messages']['collecting_info']
ANALYZING_MESSAGE = CONFIG['messages']['analyzing']
PROCESSING_ERROR_MESSAGE = CONFIG['messages']['processing_error']
EMERGENCY_WARNING_MESSAGE = CONFIG['messages']['emergency_warning']
NO_DOCTORS_FOUND_MESSAGE = CONFIG['messages']['no_doctors_found']
DOCTORS_INTRO_MESSAGE = CONFIG['messages']['doctors_intro']
CANCEL_MESSAGE = CONFIG['messages']['cancel']

# Structured flow messages
ASK_DURATION_MESSAGE = CONFIG['messages']['ask_duration']
ASK_SEVERITY_MESSAGE = CONFIG['messages']['ask_severity']
ASK_ASSOCIATED_SYMPTOMS_MESSAGE = CONFIG['messages']['ask_associated_symptoms']
ASK_AGE_MESSAGE = CONFIG['messages']['ask_age']
ASK_LOCATION_MESSAGE = CONFIG['messages']['ask_location']
ASK_CHRONIC_CONDITIONS_MESSAGE = CONFIG['messages']['ask_chronic_conditions']
ASK_CURRENT_MEDICATIONS_MESSAGE = CONFIG['messages']['ask_current_medications']

# =====================
# API Settings (from YAML)
# =====================
GROQ_TEMPERATURE = CONFIG['api']['groq']['temperature']
GROQ_MAX_TOKENS = CONFIG['api']['groq']['max_tokens']
GROQ_TRIAGE_TEMPERATURE = CONFIG['api']['groq']['triage_temperature']
GROQ_TRIAGE_MAX_TOKENS = CONFIG['api']['groq']['triage_max_tokens']

# =====================
# Prompts (from YAML)
# =====================
TRIAGE_SYSTEM_PROMPT = CONFIG['prompts']['triage_system']
CLARIFYING_QUESTION_PROMPT = CONFIG['prompts']['clarifying_question']

