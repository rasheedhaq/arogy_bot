import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock groq module
mock_groq_module = MagicMock()
sys.modules['groq'] = mock_groq_module
sys.modules['together'] = MagicMock()

import app.llm_client as llm_module
from app.llm_client import LLMClient

class TestLLMClient:
    def test_initialization(self):
        # Mock env vars and rate limits
        with patch.object(llm_module, 'GROQ_API_KEY', 'test_key'), \
             patch.object(llm_module, 'TOGETHER_API_KEY', ''), \
             patch.object(LLMClient, '_load_rate_limits', return_value={}):
            
            # We need to ensure the mock module has the Groq class
            mock_groq_module.Groq = MagicMock()
            
            client = LLMClient()
            assert len(client.providers) > 0
            assert 'groq' in [p[0] for p in client.providers]

    @patch('groq.Groq')
    def test_chat_fallback(self, mock_groq):
        # Setup mock to fail first then succeed
        mock_groq_instance = mock_groq.return_value
        mock_groq_instance.chat.completions.create.side_effect = Exception("API Error")
        
        with patch.object(llm_module, 'GROQ_API_KEY', 'test_key'), \
             patch.object(llm_module, 'TOGETHER_API_KEY', 'test_key_2'), \
             patch.object(LLMClient, '_load_rate_limits', return_value={}):
            
            # Patch Together as well
            with patch('together.Together') as mock_together:
                mock_together_instance = mock_together.return_value
                mock_together_instance.chat.completions.create.return_value.choices[0].message.content = "Success"
                
                client = LLMClient()
                
                # Verify providers are loaded
                provider_names = [p[0] for p in client.providers]
                assert 'groq' in provider_names
                assert 'together' in provider_names
                
                response = client.chat([{"role": "user", "content": "hi"}])
                assert response == "Success"

    def test_messages_to_prompt(self):
        # We can test this without initializing providers if we mock _init_providers
        # We also need to mock _load_rate_limits to avoid file access
        # AND we need to ensure __init__ doesn't raise RuntimeError by mocking it or populating providers
        
        with patch.object(LLMClient, '__init__', return_value=None) as mock_init:
            client = LLMClient()
            # Manually set providers to empty to avoid errors if accessed (though not used here)
            client.providers = [] 
            
            messages = [
                {"role": "system", "content": "Sys"},
                {"role": "user", "content": "Hi"}
            ]
            prompt = client._messages_to_prompt(messages)
            assert "Instructions: Sys" in prompt
            assert "User: Hi" in prompt
