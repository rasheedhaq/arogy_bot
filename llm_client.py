"""
LLM Client with Multi-Provider Fallback Support
Providers: Groq → Deepseek → OpenRouter → Gemini → HuggingFace → Anthropic
Implements intelligent fallback for rate limits and failures
Persistent rate limit tracking to skip failed providers
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
    GEMINI_MODEL,
    TOGETHER_API_KEY,
    TOGETHER_MODEL,
    DEEPSEEK_API_KEY,
    DEEPSEEK_MODEL,
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    HUGGINGFACE_API_KEY,
    HUGGINGFACE_MODEL,
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL
)
import json
import time
import os
from datetime import datetime, timedelta

# Lazy imports for optional providers
genai = None
InferenceClient = None
Anthropic = None

# Rate limit tracking file
RATE_LIMIT_FILE = "rate_limits.json"


class LLMClient:
    def __init__(self):
        """Initialize all available LLM providers with fallback chain"""
        self.providers = []
        self.provider_names = []
        self.rate_limited_providers = self._load_rate_limits()
        
        # Provider 1: Groq (Primary - Fast and reliable)
        if GROQ_API_KEY and not self._is_rate_limited('groq'):
            try:
                self.groq_client = Groq(api_key=GROQ_API_KEY)
                self.groq_model = MODEL_NAME
                self.providers.append(('groq', self._call_groq))
                self.provider_names.append(f"Groq ({MODEL_NAME})")
            except Exception as e:
                print(f"⚠️ Failed to initialize Groq: {e}")
        elif self._is_rate_limited('groq'):
            print(f"⏭️ Skipping Groq (rate limited until {self.rate_limited_providers.get('groq', '')})")
        
        # Provider 2: Together AI (FREE $25 credit - High quality)
        if TOGETHER_API_KEY and not self._is_rate_limited('together'):
            try:
                from together import Together
                self.together_client = Together(api_key=TOGETHER_API_KEY)
                self.together_model = TOGETHER_MODEL
                self.providers.append(('together', self._call_together))
                self.provider_names.append(f"Together ({TOGETHER_MODEL})")
            except Exception as e:
                print(f"⚠️ Failed to initialize Together AI: {e}")
        elif self._is_rate_limited('together'):
            print(f"⏭️ Skipping Together AI (rate limited until {self.rate_limited_providers.get('together', '')})")
        
        # Provider 3: Deepseek (UNLIMITED FREE)
        if DEEPSEEK_API_KEY and not self._is_rate_limited('deepseek'):
            try:
                from openai import OpenAI
                self.deepseek_client = OpenAI(
                    api_key=DEEPSEEK_API_KEY,
                    base_url="https://api.deepseek.com"
                )
                self.deepseek_model = DEEPSEEK_MODEL
                self.providers.append(('deepseek', self._call_deepseek))
                self.provider_names.append(f"Deepseek ({DEEPSEEK_MODEL})")
            except Exception as e:
                print(f"⚠️ Failed to initialize Deepseek: {e}")
        
        # Provider 4: OpenRouter (FREE models available)
        if OPENROUTER_API_KEY:
            try:
                from openai import OpenAI
                self.openrouter_client = OpenAI(
                    api_key=OPENROUTER_API_KEY,
                    base_url="https://openrouter.ai/api/v1"
                )
                self.openrouter_model = OPENROUTER_MODEL
                self.providers.append(('openrouter', self._call_openrouter))
                self.provider_names.append(f"OpenRouter ({OPENROUTER_MODEL})")
            except Exception as e:
                print(f"⚠️ Failed to initialize OpenRouter: {e}")
        
        # Provider 5: Google Gemini (Generous free tier)
        if USE_GEMINI and GEMINI_API_KEY:
            try:
                import google.generativeai as genai_module
                global genai
                genai = genai_module
                genai.configure(api_key=GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(GEMINI_MODEL)
                self.providers.append(('gemini', self._call_gemini))
                self.provider_names.append(f"Gemini ({GEMINI_MODEL})")
            except Exception as e:
                print(f"⚠️ Failed to initialize Gemini: {e}")
        
        # Provider 6: HuggingFace (Free inference API)
        if HUGGINGFACE_API_KEY and not self._is_rate_limited('huggingface'):
            try:
                from huggingface_hub import InferenceClient as HFInferenceClient
                global InferenceClient
                InferenceClient = HFInferenceClient
                self.hf_client = InferenceClient(token=HUGGINGFACE_API_KEY)
                self.hf_model = HUGGINGFACE_MODEL
                self.providers.append(('huggingface', self._call_huggingface))
                self.provider_names.append(f"HuggingFace ({HUGGINGFACE_MODEL})")
            except ImportError as e:
                print(f"⏭️ Skipping HuggingFace (import error - optional dependency)")
            except Exception as e:
                print(f"⚠️ Failed to initialize HuggingFace: {e}")
        elif self._is_rate_limited('huggingface'):
            print(f"⏭️ Skipping HuggingFace (rate limited until {self.rate_limited_providers.get('huggingface', '')})")
        
        # Provider 7: Anthropic Claude (Fallback)
        if ANTHROPIC_API_KEY:
            try:
                from anthropic import Anthropic as AnthropicClient
                global Anthropic
                Anthropic = AnthropicClient
                self.anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
                self.anthropic_model = ANTHROPIC_MODEL
                self.providers.append(('anthropic', self._call_anthropic))
                self.provider_names.append(f"Anthropic ({ANTHROPIC_MODEL})")
            except Exception as e:
                print(f"⚠️ Failed to initialize Anthropic: {e}")
        
        # Print initialized providers
        if self.providers:
            print(f"✅ LLM Providers initialized ({len(self.providers)}): {' → '.join(self.provider_names)}")
        else:
            raise RuntimeError("❌ No LLM providers available! Check API keys in .env")
    
    def _load_rate_limits(self):
        """Load rate limit data from file"""
        if os.path.exists(RATE_LIMIT_FILE):
            try:
                with open(RATE_LIMIT_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_rate_limit(self, provider_name, retry_after_minutes=1440):
        """Save rate limit with expiry time (default 24 hours)"""
        rate_limits = self._load_rate_limits()
        expiry_time = (datetime.now() + timedelta(minutes=retry_after_minutes)).isoformat()
        rate_limits[provider_name] = expiry_time
        
        with open(RATE_LIMIT_FILE, 'w') as f:
            json.dump(rate_limits, f)
        
        print(f"📝 Rate limit saved for {provider_name} until {expiry_time}")
    
    def _is_rate_limited(self, provider_name):
        """Check if provider is currently rate limited"""
        if provider_name in self.rate_limited_providers:
            expiry_str = self.rate_limited_providers[provider_name]
            try:
                expiry_time = datetime.fromisoformat(expiry_str)
                if datetime.now() < expiry_time:
                    return True
                else:
                    # Rate limit expired, remove it
                    rate_limits = self._load_rate_limits()
                    if provider_name in rate_limits:
                        del rate_limits[provider_name]
                        with open(RATE_LIMIT_FILE, 'w') as f:
                            json.dump(rate_limits, f)
            except:
                pass
        return False
    
    def chat(self, messages, temperature=None, max_tokens=None, json_mode=False):
        """
        Send messages to LLM with automatic fallback
        Tries each provider in sequence until one succeeds
        
        Args:
            messages: OpenAI-style message list
            temperature: Sampling temperature
            max_tokens: Max response tokens
            json_mode: Request JSON response format
        
        Returns:
            str: LLM response text or None if all providers fail
        """
        temp = temperature or GROQ_TEMPERATURE
        tokens = max_tokens or GROQ_MAX_TOKENS
        
        last_error = None
        
        # Try each provider in sequence
        for provider_name, provider_func in self.providers:
            try:
                response = provider_func(messages, temp, tokens, json_mode)
                if response:
                    return response
            except Exception as e:
                error_msg = str(e).lower()
                
                # Check if it's a rate limit error
                if 'rate limit' in error_msg or '429' in error_msg:
                    print(f"⚠️ {provider_name.title()} rate limit hit, trying next provider...")
                    # Save rate limit for future runs
                    self._save_rate_limit(provider_name, retry_after_minutes=1440)
                else:
                    print(f"⚠️ {provider_name.title()} error: {e}")
                
                last_error = e
                continue
        
        # All providers failed
        print(f"❌ All LLM providers failed. Last error: {last_error}")
        return None
    
    
    def _call_groq(self, messages, temperature, max_tokens, json_mode):
        """Call Groq API"""
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
        """Call Together AI API"""
        response = self.together_client.chat.completions.create(
            model=self.together_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    
    def _call_deepseek(self, messages, temperature, max_tokens, json_mode):
        """Call Deepseek API (OpenAI-compatible)"""
        response = self.deepseek_client.chat.completions.create(
            model=self.deepseek_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    
    def _call_openrouter(self, messages, temperature, max_tokens, json_mode):
        """Call OpenRouter API (OpenAI-compatible)"""
        response = self.openrouter_client.chat.completions.create(
            model=self.openrouter_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    
    def _call_gemini(self, messages, temperature, max_tokens, json_mode):
        """Call Google Gemini API"""
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        
        # Convert messages to Gemini format
        prompt = self._messages_to_prompt(messages)
        
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
        
        # Note: Gemini JSON mode is different - we'll add instruction in prompt
        if json_mode:
            prompt += "\n\nIMPORTANT: Respond with valid JSON format only, no additional text."
        
        # Safety settings to allow medical content
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
        
        # Check if response was blocked
        if not response.text:
            print(f"⚠️ Gemini response empty or blocked. Prompt feedback: {response.prompt_feedback}")
            return None
            
        return response.text
    
    
    def _call_huggingface(self, messages, temperature, max_tokens, json_mode):
        """Call HuggingFace Inference API"""
        # Convert messages to single prompt
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
            print(f"⚠️ HuggingFace error: {e}")
        # Last-resort fallback: try a public, always-free model
        try:
            from huggingface_hub import InferenceClient as HFInferenceClient
            fallback_client = HFInferenceClient()
            fallback_model = "google/flan-t5-base"
            fallback_response = fallback_client.text_generation(
                prompt,
                model=fallback_model,
                max_new_tokens=max_tokens,
                return_full_text=False
            )
            print("✅ Used last-resort HuggingFace fallback (google/flan-t5-base)")
            return fallback_response
        except Exception as e:
            print(f"❌ Last-resort HuggingFace fallback failed: {e}")
            return None
    
    
    def _call_anthropic(self, messages, temperature, max_tokens, json_mode):
        """Call Anthropic Claude API"""
        # Separate system message from conversation
        system_msg = ""
        conversation = []
        
        for msg in messages:
            if msg['role'] == 'system':
                system_msg = msg['content']
            else:
                conversation.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
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
    
    
    def _messages_to_prompt(self, messages):
        """Convert OpenAI-style messages to single prompt for Gemini/HuggingFace"""
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
        
        response = self.chat(messages, temperature=GROQ_TRIAGE_TEMPERATURE, max_tokens=GROQ_TRIAGE_MAX_TOKENS, json_mode=False)
        
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
        
        response = self.chat(messages, temperature=GROQ_TRIAGE_TEMPERATURE, max_tokens=GROQ_TRIAGE_MAX_TOKENS, json_mode=False)
        
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
        
        return self.chat(messages, temperature=GROQ_TEMPERATURE, max_tokens=150, json_mode=False)