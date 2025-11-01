"""
Telegram bot handlers with structured medical history collection
Following clinical SOAP protocol
"""
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)
from llm_client import LLMClient
from doctor_matcher import DoctorMatcher
from config import CONFIG, EMERGENCY_KEYWORDS, DEBUG
import json

# Conversation states - following medical history flow
(CHIEF_COMPLAINT, ASK_DURATION, ASK_SEVERITY, ASK_ASSOCIATED_SYMPTOMS,
 ASK_AGE, ASK_LOCATION, ASK_CHRONIC_CONDITIONS, ASK_MEDICATIONS, FINAL_TRIAGE) = range(9)

# Initialize clients
llm_client = LLMClient()
doctor_matcher = DoctorMatcher()


def debug_log(label, data):
    """Print debug information in terminal (only when DEBUG=true)"""
    if DEBUG:
        print(f"\n{'='*60}")
        print(f"🔍 DEBUG: {label}")
        print(f"{'='*60}")
        if isinstance(data, dict):
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(data)
        print(f"{'='*60}\n")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start conversation - collect chief complaint"""
    debug_log("START Command", {
        "user_id": update.effective_user.id,
        "username": update.effective_user.username,
        "message": update.message.text
    })
    
    # Initialize patient data
    context.user_data.clear()
    context.user_data['patient_data'] = {}
    
    # If user sent a message (not /start), treat it as chief complaint
    if update.message.text and not update.message.text.startswith('/start'):
        # Welcome them first
        await update.message.reply_text(f"{CONFIG["messages"]["emergency"]}\n\n{CONFIG["messages"]["welcome"]}")
        
        # Store their complaint and move to next question
        chief_complaint = update.message.text.strip()
        
        # Check for emergency keywords
        if any(keyword in chief_complaint.lower() for keyword in EMERGENCY_KEYWORDS):
            await update.message.reply_text(CONFIG["messages"]["emergency_detected"])
            return ConversationHandler.END
        
        context.user_data['patient_data']['chief_complaint'] = chief_complaint
        await update.message.reply_text(CONFIG["messages"]["ask_duration"])
        return ASK_DURATION
    
    # Normal /start command
    await update.message.reply_text(f"{CONFIG["messages"]["emergency"]}\n\n{CONFIG["messages"]["welcome"]}")
    return CHIEF_COMPLAINT


async def handle_chief_complaint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect chief complaint - with intelligent parsing"""
    chief_complaint = update.message.text.strip()
    debug_log("Chief Complaint", {"complaint": chief_complaint})
    
    # Check for emergency
    if any(keyword in chief_complaint.lower() for keyword in EMERGENCY_KEYWORDS):
        await update.message.reply_text(CONFIG["messages"]["emergency_detected"])
        return ConversationHandler.END
    
    # INTELLIGENT PARSING: Check if message is detailed enough for direct triage
    message_lower = chief_complaint.lower()
    word_count = len(chief_complaint.split())
    
    # If message is detailed (>10 words) or contains key indicators, try intelligent extraction
    if word_count >= 10 or any(indicator in message_lower for indicator in 
        ['having', 'experiencing', 'suffering', 'feeling', 'pain in', 'since', 'for', 'days', 'weeks', 'severe', 'mild']):
        
        debug_log("Attempting Intelligent Parse", {"message": chief_complaint})
        
        # Try to extract complete info using LLM
        quick_triage = llm_client.extract_triage_info_structured({
            'chief_complaint': chief_complaint,
            'duration': 'not specified',
            'severity': 'not specified',
            'associated_symptoms': 'not specified',
            'age': 'not specified',
            'location': 'not specified',
            'chronic_conditions': 'none',
            'medications': 'none'
        })
        
        if quick_triage and quick_triage.get('specialty'):
            debug_log("Intelligent Parse SUCCESS - Skipping Questions", quick_triage)
            
            # Store the parsed data
            context.user_data['patient_data']['chief_complaint'] = chief_complaint
            
            await update.message.reply_text(
                f"I understand you're experiencing {chief_complaint}. "
                f"Let me find the right specialist for you..."
            )
            
            # Find doctors directly
            symptoms = quick_triage.get('symptoms') or []
            if isinstance(symptoms, str):
                symptoms = [symptoms]
            specialty = quick_triage.get('specialty') or 'General Physician'
            
            matches = doctor_matcher.find_doctors(
                symptoms=symptoms,
                specialty=specialty,
                online_only=False,
                limit=CONFIG["conversation"]["max_doctor_results"]
            )
            
            debug_log("Quick Match Results", {
                "count": len(matches),
                "doctors": [m['doctor'].get('full_name', m['doctor'].get('Doctor_Name')) for m in matches]
            })
            
            if matches:
                response = CONFIG["messages"]["doctors_intro"].format(specialty=specialty, count=len(matches))
                await update.message.reply_text(response)
                
                for match in matches:
                    card = doctor_matcher.format_doctor_card(match)
                    await update.message.reply_text(card, parse_mode='Markdown')
                
                await update.message.reply_text(CONFIG["messages"]["disclaimer"])
                return ConversationHandler.END
    
    # If not enough detail, continue with standard questions
    debug_log("Standard Flow - Asking Questions", {"reason": "Insufficient detail or simple complaint"})
    context.user_data['patient_data']['chief_complaint'] = chief_complaint
    await update.message.reply_text(CONFIG["messages"]["ask_duration"])
    return ASK_DURATION


async def handle_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect duration of symptoms"""
    duration = update.message.text.strip()
    
    # Handle non-helpful responses
    if duration.lower() in ['no', 'idk', 'i dont know', 'na', 'n/a', 'skip', 'nothing']:
        duration = 'not specified'
    
    context.user_data['patient_data']['duration'] = duration
    debug_log("Duration", {"duration": duration})
    
    await update.message.reply_text(CONFIG["messages"]["ask_severity"])
    return ASK_SEVERITY


async def handle_severity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect severity"""
    severity = update.message.text.strip()
    
    # Handle non-helpful responses
    if severity.lower() in ['no', 'idk', 'i dont know', 'na', 'n/a', 'skip', 'nothing']:
        severity = 'moderate'  # Default assumption
    
    context.user_data['patient_data']['severity'] = severity
    
    await update.message.reply_text(CONFIG["messages"]["ask_associated_symptoms"])
    return ASK_ASSOCIATED_SYMPTOMS


async def handle_associated_symptoms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect associated symptoms"""
    associated_symptoms = update.message.text.strip()
    context.user_data['patient_data']['associated_symptoms'] = associated_symptoms
    
    await update.message.reply_text(CONFIG["messages"]["ask_age"])
    return ASK_AGE


async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect patient age"""
    age = update.message.text.strip()
    context.user_data['patient_data']['age'] = age
    
    await update.message.reply_text(CONFIG["messages"]["ask_location"])
    return ASK_LOCATION


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect patient location"""
    location = update.message.text.strip()
    context.user_data['patient_data']['location'] = location
    
    await update.message.reply_text(CONFIG["messages"]["ask_chronic_conditions"])
    return ASK_CHRONIC_CONDITIONS


async def handle_chronic_conditions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect chronic conditions"""
    chronic_conditions = update.message.text.strip()
    context.user_data['patient_data']['chronic_conditions'] = chronic_conditions
    
    await update.message.reply_text(CONFIG["messages"]["ask_current_medications"])
    return ASK_MEDICATIONS


async def handle_medications_and_triage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collect medications and perform final triage"""
    medications = update.message.text.strip()
    context.user_data['patient_data']['medications'] = medications
    
    # Now we have all the data - perform triage
    await update.message.reply_text(CONFIG["messages"]["analyzing"])
    
    patient_data = context.user_data['patient_data']
    debug_log("Complete Patient Data", patient_data)
    
    triage_info = llm_client.extract_triage_info_structured(patient_data)
    debug_log("AI Triage Analysis", triage_info)
    
    if not triage_info:
        await update.message.reply_text(CONFIG["messages"]["processing_error"])
        return ConversationHandler.END
    
    # Check for emergency
    if triage_info.get('is_emergency', False):
        await update.message.reply_text(CONFIG["messages"]["emergency_warning"])
    
    # Find matching doctors
    symptoms = triage_info.get('symptoms') or []
    if isinstance(symptoms, str):
        symptoms = [symptoms]
    specialty = triage_info.get('specialty') or 'General Physician'
    
    debug_log("Doctor Search Parameters", {
        "symptoms": symptoms,
        "specialty": specialty
    })
    
    matches = doctor_matcher.find_doctors(
        symptoms=symptoms,
        specialty=specialty,
        online_only=False,
        limit=CONFIG["conversation"]["max_doctor_results"]
    )
    
    debug_log("Doctor Matches Found", {
        "count": len(matches),
        "doctors": [m['doctor'].get('full_name', m['doctor'].get('Doctor_Name')) for m in matches]
    })
    
    if not matches:
        await update.message.reply_text(
            CONFIG["messages"]["no_doctors_found"].format(specialty=specialty)
            + f"\n\n{CONFIG['messages']['disclaimer']}"
        )
        return ConversationHandler.END
    
    # Send results
    response = CONFIG["messages"]["doctors_intro"].format(specialty=specialty, count=len(matches))
    await update.message.reply_text(response)
    
    for match in matches:
        card = doctor_matcher.format_doctor_card(match)
        await update.message.reply_text(card, parse_mode='Markdown')
    
    await update.message.reply_text(
        f"\n{CONFIG['messages']['disclaimer']}\n\n"
        "Type /start for a new search."
    )
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    context.user_data.clear()
    await update.message.reply_text(CONFIG["messages"]["cancel"])
    return ConversationHandler.END


def setup_handlers(application):
    """Setup conversation handlers with structured flow"""
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.TEXT & ~filters.COMMAND, start)
        ],
        states={
            CHIEF_COMPLAINT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chief_complaint)
            ],
            ASK_DURATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_duration)
            ],
            ASK_SEVERITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_severity)
            ],
            ASK_ASSOCIATED_SYMPTOMS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_associated_symptoms)
            ],
            ASK_AGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age)
            ],
            ASK_LOCATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location)
            ],
            ASK_CHRONIC_CONDITIONS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chronic_conditions)
            ],
            ASK_MEDICATIONS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_medications_and_triage)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(conv_handler)
