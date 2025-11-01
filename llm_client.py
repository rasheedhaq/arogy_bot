"""
LLM Client for interacting with Groq API and Google Gemini
Implements fallback logic for reliability
"""
from groq import Groq
from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    GROQ_TEMPERATURE,
    GROQ_MAX_TOKENS,
    GROQ_TRIAGE_TEMPERATURE,
    GROQ_TRIAGE_MAX_TOKENS,
    TRIAGE_SYSTEM_PROMPT,
    CLARIFYING_QUESTION_PROMPT,
    MAX_CLARIFYING_QUESTIONS,
    GEMINI_API_KEY,
    USE_GEMINI,
    GEMINI_MODEL
)
import json

# Gemini will be imported lazily to avoid dependency issues
genai = None
GEMINI_AVAILABLE = False


class LLMClient:
    def __init__(self):
        global genai, GEMINI_AVAILABLE
        
        # Initialize Groq (fallback)
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.groq_model = MODEL_NAME
        
        # Try to import and initialize Gemini if configured
        self.use_gemini = False
        if USE_GEMINI and GEMINI_API_KEY:
            try:
                import google.generativeai as genai_module
                genai = genai_module
                GEMINI_AVAILABLE = True
                
                genai.configure(api_key=GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(GEMINI_MODEL)
                self.use_gemini = True
                print(f"✅ Using Gemini {GEMINI_MODEL} with Groq {MODEL_NAME} fallback")
            except Exception as e:
                print(f"⚠️ Failed to initialize Gemini: {e}")
                print(f"✅ Using Groq {MODEL_NAME} only")
        else:
            print(f"✅ Using Groq {MODEL_NAME}")
    
    
    def chat(self, messages, temperature=None, max_tokens=None):
        """
        Send messages to LLM and get response
        Uses Gemini first, falls back to Groq
        """
        temp = temperature or GROQ_TEMPERATURE
        tokens = max_tokens or GROQ_MAX_TOKENS
        
        # Try Gemini first if enabled
        if self.use_gemini:
            try:
                # Convert messages to Gemini format
                prompt = self._messages_to_prompt(messages)
                
                generation_config = {
                    "temperature": temp,
                    "max_output_tokens": tokens,
                }
                
                response = self.gemini_model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                return response.text
            except Exception as e:
                print(f"⚠️ Gemini failed: {e}, falling back to Groq")
                # Fall through to Groq
        
        # Use Groq (either as primary or fallback)
        try:
            response = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=messages,
                temperature=temp,
                max_tokens=tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            return None
    
    def _messages_to_prompt(self, messages):
        """Convert OpenAI-style messages to single prompt for Gemini"""
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                prompt_parts.append(f"Instructions: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        return "\n\n".join(prompt_parts)
    
    def extract_triage_info_structured(self, patient_data):
        """
        Extract triage information from structured patient data
        Following clinical protocol
        """
        # Format the prompt with actual patient data
        formatted_prompt = TRIAGE_SYSTEM_PROMPT.format(
            chief_complaint=patient_data.get('chief_complaint', 'not specified'),
            duration=patient_data.get('duration', 'not specified'),
            severity=patient_data.get('severity', 'not specified'),
            associated_symptoms=patient_data.get('associated_symptoms', 'none'),
            age=patient_data.get('age', 'not specified'),
            location=patient_data.get('location', 'not specified'),
            chronic_conditions=patient_data.get('chronic_conditions', 'none'),
            medications=patient_data.get('medications', 'none')
        )
        
        messages = [
            {"role": "system", "content": "You are a medical triage AI assistant."},
            {"role": "user", "content": formatted_prompt}
        ]
        
        response = self.chat(messages, temperature=GROQ_TRIAGE_TEMPERATURE, max_tokens=GROQ_TRIAGE_MAX_TOKENS)
        
        try:
            if response:
                # Find JSON in response
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = response[start:end]
                    data = json.loads(json_str)
                    # Apply sensible fallbacks when model omits fields
                    if not isinstance(data, dict):
                        return None
                    data.setdefault('specialty', 'General Physician')
                    symptoms = data.get('symptoms')
                    if isinstance(symptoms, str) and symptoms:
                        data['symptoms'] = [symptoms]
                    elif symptoms is None:
                        data['symptoms'] = []
                    return data
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {response}")
            print(f"Error: {e}")
        
        return None
    
    def extract_triage_info(self, conversation_history):
        """
        Extract symptoms, severity, and specialty from conversation
        (Legacy method - kept for compatibility)
        """
        messages = [
            {"role": "system", "content": "You are a medical triage assistant."},
            {"role": "user", "content": f"Conversation: {conversation_history}"}
        ]
        
        response = self.chat(messages, temperature=GROQ_TRIAGE_TEMPERATURE, max_tokens=GROQ_TRIAGE_MAX_TOKENS)
        
        try:
            # Try to extract JSON from response
            if response:
                # Find JSON in response
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = response[start:end]
                    return json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON: {response}")
        
        return None
    
    def generate_clarifying_question(self, conversation_history, question_count):
        """
        Generate a clarifying question based on conversation
        """
        system_prompt = CLARIFYING_QUESTION_PROMPT.format(
            question_count=question_count,
            max_questions=MAX_CLARIFYING_QUESTIONS
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Conversation so far: {conversation_history}"}
        ]
        
        return self.chat(messages, temperature=GROQ_TEMPERATURE, max_tokens=150)