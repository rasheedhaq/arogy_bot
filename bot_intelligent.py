"""
Intelligent conversational bot - LLM-driven medical conversation
Acts like a real doctor conducting a natural consultation
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

# Single conversation state
CONSULTING = 1

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
    """Start conversation"""
    debug_log("START Command", {
        "user_id": update.effective_user.id,
        "username": update.effective_user.username
    })
    
    # Initialize conversation history
    context.user_data.clear()
    context.user_data['conversation_history'] = []
    context.user_data['collected_info'] = {}
    
    welcome_msg = f"{CONFIG['messages']['emergency']}\n\n{CONFIG['messages']['welcome']}"
    await update.message.reply_text(welcome_msg)
    
    return CONSULTING


async def handle_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle natural conversation - LLM decides next question"""
    user_message = update.message.text.strip()
    
    debug_log(">>> INCOMING MESSAGE", {
        "user": update.effective_user.username,
        "message": user_message,
        "message_id": update.message.message_id
    })
    
    # Add to conversation history
    conversation_history = context.user_data.get('conversation_history', [])
    conversation_history.append({
        "role": "patient",
        "message": user_message
    })
    
    debug_log("Patient Message", {"message": user_message})
    
    # Check for emergency keywords
    if any(keyword in user_message.lower() for keyword in EMERGENCY_KEYWORDS):
        await update.message.reply_text(CONFIG["messages"]["emergency_detected"])
        return ConversationHandler.END
    
    # Build conversation context for LLM
    conversation_context = "\n".join([
        f"{'Patient' if msg['role'] == 'patient' else 'Doctor'}: {msg['message']}"
        for msg in conversation_history
    ])
    
    # Ask LLM to act as doctor and decide next step
    doctor_response = await get_doctor_response(conversation_context, context.user_data.get('collected_info', {}))
    
    debug_log("Doctor's Decision", doctor_response)
    
    # Update collected info
    if doctor_response.get('extracted_info'):
        context.user_data['collected_info'].update(doctor_response['extracted_info'])
    
    # Check if enough information collected
    if doctor_response.get('ready_for_recommendation'):
        # Find doctors
        specialty = doctor_response.get('specialty', 'General Physician')
        symptoms = doctor_response.get('symptoms', [])
        
        debug_log("Finding Doctors", {
            "specialty": specialty,
            "symptoms": symptoms
        })
        
        matches = doctor_matcher.find_doctors(
            symptoms=symptoms,
            specialty=specialty,
            online_only=False,
            limit=CONFIG["conversation"]["max_doctor_results"]
        )
        
        debug_log("Matches Found", {
            "count": len(matches),
            "doctors": [m['doctor'].get('full_name', m['doctor'].get('Doctor_Name')) for m in matches]
        })
        
        # Send doctor's final message
        await update.message.reply_text(doctor_response['message'])
        
        if matches:
            intro = f"Based on your symptoms, I recommend seeing a {specialty}. Here are some specialists:"
            await update.message.reply_text(intro)
            
            for match in matches:
                card = doctor_matcher.format_doctor_card(match)
                await update.message.reply_text(card, parse_mode='Markdown')
            
            await update.message.reply_text(CONFIG["messages"]["disclaimer"])
        else:
            await update.message.reply_text(
                f"I'd recommend seeing a {specialty}, but I don't have any specialists in our database right now. "
                f"Please consult with a local {specialty}.\n\n{CONFIG['messages']['disclaimer']}"
            )
        
        return ConversationHandler.END
    else:
        # Continue conversation - ask next question
        conversation_history.append({
            "role": "doctor",
            "message": doctor_response['message']
        })
        context.user_data['conversation_history'] = conversation_history
        
        await update.message.reply_text(doctor_response['message'])
        return CONSULTING


async def get_doctor_response(conversation_context: str, collected_info: dict):
    """
    Use LLM to act as a doctor and decide next question or recommendation
    """
    
    system_prompt = """You are an experienced medical doctor conducting a patient consultation via chat.

Your goals:
1. Gather essential information naturally (chief complaint, duration, severity, associated symptoms, relevant medical history)
2. Ask ONE question at a time, like a real doctor would
3. Be empathetic, professional, and conversational
4. Once you have enough information, provide a specialty recommendation

Medical protocol to follow:
- Chief Complaint: What's bothering them?
- History of Present Illness: Duration, severity, progression
- Associated Symptoms: What else are they experiencing?
- Relevant Medical History: Chronic conditions, medications (only if relevant)
- Red Flags: Emergency symptoms requiring immediate care

IMPORTANT: After 3-4 exchanges, you MUST have enough information to make a recommendation.
Set "ready_for_recommendation": true when you have:
1. Chief complaint identified
2. Duration known (even if approximate)
3. Severity assessed (even if patient described it loosely)
4. Key associated symptoms noted

Don't over-ask! Real doctors make decisions with limited info.

Response format (JSON):
{
  "message": "Your next question or final assessment",
  "ready_for_recommendation": false,
  "extracted_info": {
    "chief_complaint": "...",
    "duration": "...",
    "severity": "...",
    "associated_symptoms": ["..."],
    "red_flags": ["..."]
  },
  "specialty": "Dentist/Cardiologist/etc",
  "symptoms": ["symptom1", "symptom2"],
  "reasoning": "Why you're asking this or making this recommendation"
}

Rules:
- Keep questions SHORT and friendly
- Don't ask multiple questions at once
- Use everyday language, not medical jargon
- After 3-4 exchanges, you should have enough info to recommend
- Be concise - 1-2 sentences max per message
"""

    user_prompt = f"""Conversation so far:
{conversation_context}

Information collected:
{json.dumps(collected_info, indent=2)}

What should you (the doctor) say or ask next?"""

    # Call LLM with fallback support
    response_text = llm_client.chat(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=500,
        json_mode=True
    )
    
    if not response_text:
        # Fallback if all providers fail
        return {
            "message": "I apologize, but I'm having technical difficulties. Please describe your symptoms and I'll try to help.",
            "ready_for_recommendation": False,
            "extracted_info": {}
        }
    
    result = json.loads(response_text)
    
    # Ensure defaults
    if 'ready_for_recommendation' not in result:
        result['ready_for_recommendation'] = False
    if 'extracted_info' not in result:
        result['extracted_info'] = {}
    
    return result


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text("Consultation ended. Take care! Type /start to begin again.")
    return ConversationHandler.END


def setup_handlers(application):
    """Setup conversation handlers"""
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start)
        ],
        states={
            CONSULTING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_conversation)
            ]
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start)
        ],
        allow_reentry=True
    )
    
    application.add_handler(conv_handler)
    
    return application
