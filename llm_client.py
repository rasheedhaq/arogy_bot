"""
LLM Client with Multi-Provider Fallback Support
Providers: Groq → Deepseek → OpenRouter → Gemini → HuggingFace → Anthropic
Implements intelligent fallback for rate limits and failures
Persistent rate limit tracking to skip failed providers
"""
import json
import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple, Callable
import logging

from config import (
    GROQ_API_KEY, MODEL_NAME, GROQ_TEMPERATURE, GROQ_MAX_TOKENS,
    GROQ_TRIAGE_TEMPERATURE, GROQ_TRIAGE_MAX_TOKENS,
    TRIAGE_SYSTEM_PROMPT, CLARIFYING_QUESTION_PROMPT, MAX_CLARIFYING_QUESTIONS,
    GEMINI_API_KEY, USE_GEMINI, GEMINI_MODEL,
    TOGETHER_API_KEY, TOGETHER_MODEL,
    DEEPSEEK_API_KEY, DEEPSEEK_MODEL,
    OPENROUTER_API_KEY, OPENROUTER_MODEL,
    HUGGINGFACE_API_KEY, HUGGINGFACE_MODEL,
    ANTHROPIC_API_KEY, ANTHROPIC_MODEL
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limit tracking file
RATE_LIMIT_FILE = "rate_limits.json"

class LLMClient:
    def __init__(self):
        """Initialize all available LLM providers with fallback chain"""
        self.providers: List[Tuple[str, Callable]] = []
        self.provider_names: List[str] = []
        self.rate_limited_providers = self._load_rate_limits()
        
        self._init_providers()
        
        if self.providers:
            logger.info(f"✅ LLM Providers initialized ({len(self.providers)}): {' → '.join(self.provider_names)}")
        else:
            raise RuntimeError("❌ No LLM providers available! Check API keys in .env")

    def _init_providers(self):
        """Initialize providers in priority order"""
        # 1. Groq
        self._try_init_provider('groq', GROQ_API_KEY, self._init_groq)
        
        # 2. Together AI
        self._try_init_provider('together', TOGETHER_API_KEY, self._init_together)
        
        # 3. Deepseek
        self._try_init_provider('deepseek', DEEPSEEK_API_KEY, self._init_deepseek)
        
        # 4. OpenRouter
        self._try_init_provider('openrouter', OPENROUTER_API_KEY, self._init_openrouter)
        
        # 5. Gemini
        if USE_GEMINI:
            self._try_init_provider('gemini', GEMINI_API_KEY, self._init_gemini)
        
        # 6. HuggingFace
        self._try_init_provider('huggingface', HUGGINGFACE_API_KEY, self._init_huggingface)
        
        # 7. Anthropic
        self._try_init_provider('anthropic', ANTHROPIC_API_KEY, self._init_anthropic)

    def _try_init_provider(self, name: str, api_key: str, init_func: Callable):
        """Helper to safely initialize a provider if key exists and not rate limited"""
        if not api_key:
            return
            
        if self._is_rate_limited(name):
            logger.warning(f"⏭️ Skipping {name.title()} (rate limited until {self.rate_limited_providers.get(name, '')})")
            return

        try:
            init_func(api_key)
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize {name.title()}: {e}")

    def _init_groq(self, api_key: str):
        from groq import Groq
        self.groq_client = Groq(api_key=api_key)
        self.groq_model = MODEL_NAME
        self.providers.append(('groq', self._call_groq))
        self.provider_names.append(f"Groq ({MODEL_NAME})")

    def _init_together(self, api_key: str):
        from together import Together
        self.together_client = Together(api_key=api_key)
        self.together_model = TOGETHER_MODEL
        self.providers.append(('together', self._call_together))
        self.provider_names.append(f"Together ({TOGETHER_MODEL})")

    def _init_deepseek(self, api_key: str):
        from openai import OpenAI
        self.deepseek_client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.deepseek_model = DEEPSEEK_MODEL
        self.providers.append(('deepseek', self._call_deepseek))
        self.provider_names.append(f"Deepseek ({DEEPSEEK_MODEL})")

    def _init_openrouter(self, api_key: str):
        from openai import OpenAI
        self.openrouter_client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        self.openrouter_model = OPENROUTER_MODEL
        self.providers.append(('openrouter', self._call_openrouter))
        self.provider_names.append(f"OpenRouter ({OPENROUTER_MODEL})")

    def _init_gemini(self, api_key: str):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel(GEMINI_MODEL)
        self.providers.append(('gemini', self._call_gemini))
        self.provider_names.append(f"Gemini ({GEMINI_MODEL})")

    def _init_huggingface(self, api_key: str):
        from huggingface_hub import InferenceClient
        self.hf_client = InferenceClient(token=api_key)
        self.hf_model = HUGGINGFACE_MODEL
        self.providers.append(('huggingface', self._call_huggingface))
        self.provider_names.append(f"HuggingFace ({HUGGINGFACE_MODEL})")

    def _init_anthropic(self, api_key: str):
        from anthropic import Anthropic
        self.anthropic_client = Anthropic(api_key=api_key)
        self.anthropic_model = ANTHROPIC_MODEL
        self.providers.append(('anthropic', self._call_anthropic))
        self.provider_names.append(f"Anthropic ({ANTHROPIC_MODEL})")

    def _load_rate_limits(self) -> Dict[str, str]:
        if os.path.exists(RATE_LIMIT_FILE):
            try:
                with open(RATE_LIMIT_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_rate_limit(self, provider_name: str, retry_after_minutes: int = 1440):
        rate_limits = self._load_rate_limits()
        expiry_time = (datetime.now() + timedelta(minutes=retry_after_minutes)).isoformat()
        rate_limits[provider_name] = expiry_time
        
        with open(RATE_LIMIT_FILE, 'w') as f:
            json.dump(rate_limits, f)
        
        logger.info(f"📝 Rate limit saved for {provider_name} until {expiry_time}")

    def _is_rate_limited(self, provider_name: str) -> bool:
        if provider_name in self.rate_limited_providers:
            expiry_str = self.rate_limited_providers[provider_name]
            try:
                expiry_time = datetime.fromisoformat(expiry_str)
                if datetime.now() < expiry_time:
                    return True
                else:
                    # Expired, remove it
                    rate_limits = self._load_rate_limits()
                    if provider_name in rate_limits:
                        del rate_limits[provider_name]
                        with open(RATE_LIMIT_FILE, 'w') as f:
                            json.dump(rate_limits, f)
            except:
                pass
        return False

    def chat(self, messages: List[Dict[str, str]], temperature: float = None, max_tokens: int = None, json_mode: bool = False) -> Optional[str]:
        """
        Send messages to LLM with automatic fallback.
        """
        temp = temperature or GROQ_TEMPERATURE
        tokens = max_tokens or GROQ_MAX_TOKENS
        
        last_error = None
        
        for provider_name, provider_func in self.providers:
            try:
                response = provider_func(messages, temp, tokens, json_mode)
                if response:
                    return response
            except Exception as e:
                error_msg = str(e).lower()
                if 'rate limit' in error_msg or '429' in error_msg:
                    logger.warning(f"⚠️ {provider_name.title()} rate limit hit, trying next provider...")
                    self._save_rate_limit(provider_name)
                else:
                    logger.warning(f"⚠️ {provider_name.title()} error: {e}")
                
                last_error = e
                continue
        
        logger.error(f"❌ All LLM providers failed. Last error: {last_error}")
        return None

    # --- Provider Implementations ---

    def _call_groq(self, messages, temperature, max_tokens, json_mode):
        kwargs = {
            "model": self.groq_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = self.groq_client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    def _call_together(self, messages, temperature, max_tokens, json_mode):
        # Together doesn't support response_format="json_object" natively in all models, 
        # but we can pass it if supported. For now, keeping it simple.
        response = self.together_client.chat.completions.create(
            model=self.together_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def _call_deepseek(self, messages, temperature, max_tokens, json_mode):
        kwargs = {
            "model": self.deepseek_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if json_mode:
             kwargs["response_format"] = {"type": "json_object"}
             
        response = self.deepseek_client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    def _call_openrouter(self, messages, temperature, max_tokens, json_mode):
        response = self.openrouter_client.chat.completions.create(
            model=self.openrouter_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def _call_gemini(self, messages, temperature, max_tokens, json_mode):
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        
        prompt = self._messages_to_prompt(messages)
        if json_mode:
            prompt += "\n\nIMPORTANT: Respond with valid JSON format only, no additional text."
        
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
        
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        response = self.gemini_model.generate_content(
            prompt, 
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        if not response.text:
            logger.warning(f"⚠️ Gemini response empty or blocked. Prompt feedback: {response.prompt_feedback}")
            return None
        return response.text

    def _call_huggingface(self, messages, temperature, max_tokens, json_mode):
        prompt = self._messages_to_prompt(messages)
        if json_mode:
            prompt += "\n\nIMPORTANT: Respond ONLY with valid JSON, no other text."
        
        try:
            response = self.hf_client.text_generation(
                prompt,
                model=self.hf_model,
                temperature=temperature,
                max_new_tokens=max_tokens,
                return_full_text=False
            )
            if response:
                return response
        except Exception as e:
            logger.warning(f"⚠️ HuggingFace error: {e}")
            
        # Fallback
        try:
            from huggingface_hub import InferenceClient
            fallback_client = InferenceClient()
            return fallback_client.text_generation(
                prompt,
                model="google/flan-t5-base",
                max_new_tokens=max_tokens,
                return_full_text=False
            )
        except Exception as e:
            logger.error(f"❌ Last-resort HuggingFace fallback failed: {e}")
            return None

    def _call_anthropic(self, messages, temperature, max_tokens, json_mode):
        system_msg = ""
        conversation = []
        for msg in messages:
            if msg['role'] == 'system':
                system_msg = msg['content']
            else:
                conversation.append({'role': msg['role'], 'content': msg['content']})
        
        kwargs = {
            "model": self.anthropic_model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": conversation
        }
        if system_msg:
            kwargs["system"] = system_msg
            
        response = self.anthropic_client.messages.create(**kwargs)
        return response.content[0].text

    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert OpenAI-style messages to single prompt"""
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
        """Extract triage information from structured patient data"""
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
        
        response = self.chat(messages, temperature=GROQ_TRIAGE_TEMPERATURE, max_tokens=GROQ_TRIAGE_MAX_TOKENS, json_mode=False)
        
        try:
            if response:
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = response[start:end]
                    data = json.loads(json_str)
                    if not isinstance(data, dict): return None
                    data.setdefault('specialty', 'General Physician')
                    symptoms = data.get('symptoms')
                    if isinstance(symptoms, str) and symptoms:
                        data['symptoms'] = [symptoms]
                    elif symptoms is None:
                        data['symptoms'] = []
                    return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
        
        return None

    def generate_clarifying_question(self, conversation_history, question_count):
        """Generate a clarifying question"""
        system_prompt = CLARIFYING_QUESTION_PROMPT.format(
            question_count=question_count,
            max_questions=MAX_CLARIFYING_QUESTIONS
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Conversation so far: {conversation_history}"}
        ]
        
        return self.chat(messages, temperature=GROQ_TEMPERATURE, max_tokens=150, json_mode=False)