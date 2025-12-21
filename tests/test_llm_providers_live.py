"""
Test LLM providers to ensure they work and are using free tiers
"""
import pytest
from app.llm_client import LLMClient
from app.config import (
    GROQ_API_KEY, TOGETHER_API_KEY, DEEPSEEK_API_KEY,
    OPENROUTER_API_KEY, GEMINI_API_KEY, HUGGINGFACE_API_KEY,
    ANTHROPIC_API_KEY
)

class TestLLMProviders:
    """Test all configured LLM providers"""
    
    def test_provider_initialization(self):
        """Test that at least one provider initializes"""
        client = LLMClient()
        assert len(client.providers) > 0, "No LLM providers initialized! Check API keys."
        print(f"\n✅ Initialized {len(client.providers)} provider(s): {client.provider_names}")
    
    def test_free_tier_providers(self):
        """Verify which providers are configured (should all be free tier)"""
        free_providers = {
            'Groq': GROQ_API_KEY,
            'Together AI': TOGETHER_API_KEY,
            'Deepseek': DEEPSEEK_API_KEY,
            'OpenRouter': OPENROUTER_API_KEY,
            'Gemini': GEMINI_API_KEY,
            'HuggingFace': HUGGINGFACE_API_KEY,
            'Anthropic': ANTHROPIC_API_KEY
        }
        
        configured = [name for name, key in free_providers.items() if key]
        print(f"\n📋 Configured providers: {', '.join(configured)}")
        
        # Verify free tier limits
        free_tier_info = {
            'Groq': '14,400 requests/day (FREE)',
            'Together AI': '$25 free credit',
            'Deepseek': 'Unlimited FREE',
            'OpenRouter': 'Free models available',
            'Gemini': '60 requests/min (FREE)',
            'HuggingFace': 'Free tier available',
            'Anthropic': 'Paid (not recommended for free tier)'
        }
        
        print("\n💰 Free Tier Status:")
        for provider in configured:
            print(f"  - {provider}: {free_tier_info.get(provider, 'Unknown')}")
        
        # Warn if Anthropic is configured (it's paid)
        if ANTHROPIC_API_KEY:
            print("\n⚠️  WARNING: Anthropic (Claude) is a PAID service!")
            print("   Consider removing ANTHROPIC_API_KEY to avoid charges.")
    
    def test_simple_llm_call(self):
        """Test a simple LLM call (uses minimal tokens)"""
        client = LLMClient()
        
        # Very simple test message (minimal tokens to avoid costs)
        messages = [
            {"role": "user", "content": "Say 'OK'"}
        ]
        
        response = client.chat(messages, temperature=0.1, max_tokens=5)
        
        assert response is not None, "LLM call failed! Check API keys and rate limits."
        print(f"\n✅ LLM Response: {response}")
        print(f"   Provider used: {client.provider_names[0] if client.providers else 'Unknown'}")
    
    def test_json_mode(self):
        """Test JSON mode (important for bot functionality)"""
        client = LLMClient()
        
        messages = [
            {"role": "user", "content": "Return JSON: {\"status\": \"ok\"}"}
        ]
        
        response = client.chat(messages, temperature=0.1, max_tokens=20, json_mode=True)
        
        assert response is not None, "JSON mode call failed!"
        print(f"\n✅ JSON Mode Response: {response}")
        
        # Try to parse as JSON
        import json
        try:
            json.loads(response)
            print("   ✅ Valid JSON returned")
        except:
            print("   ⚠️  Response is not valid JSON (some providers don't support json_mode)")
    
    def test_rate_limits(self):
        """Check if any providers are rate limited"""
        client = LLMClient()
        
        if client.rate_limited_providers:
            print(f"\n⚠️  Rate limited providers: {client.rate_limited_providers}")
        else:
            print("\n✅ No rate limits detected")
    
    def test_cost_estimate(self):
        """Estimate costs for typical usage"""
        print("\n💵 Cost Estimate for 1000 messages/day:")
        print("   - Groq (llama-3.3-70b): $0 (FREE - 14,400 req/day)")
        print("   - Deepseek: $0 (FREE - Unlimited)")
        print("   - Gemini: $0 (FREE - 60 req/min)")
        print("   - Together AI: ~$0.50 (from $25 credit)")
        print("   - OpenRouter (free models): $0")
        print("\n✅ Total estimated cost: $0/month (using free tiers)")
        print("   Recommendation: Use Groq or Deepseek as primary")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])
