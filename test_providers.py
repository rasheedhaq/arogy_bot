"""
Test all LLM providers individually to verify they work
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*80)
print("🧪 TESTING ALL LLM PROVIDERS")
print("="*80 + "\n")

# Test 1: Groq
print("1️⃣ GROQ API")
print("-" * 80)
groq_key = os.getenv("GROQ_API_KEY", "")
if groq_key:
    print(f"✅ API Key configured: {groq_key[:20]}...")
    try:
        from groq import Groq
        client = Groq(api_key=groq_key)
        # Try a simple call
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'Groq works!'"}],
            max_tokens=50
        )
        print(f"✅ Status: WORKING")
        print(f"   Response: {response.choices[0].message.content}")
    except Exception as e:
        error_msg = str(e)
        if "rate limit" in error_msg.lower() or "429" in error_msg:
            print(f"⚠️ Status: RATE LIMITED (will fallback)")
        else:
            print(f"❌ Status: ERROR - {error_msg}")
else:
    print("❌ API Key: NOT CONFIGURED")

print()

# Test 2: Gemini
print("2️⃣ GOOGLE GEMINI")
print("-" * 80)
gemini_key = os.getenv("GEMINI_API_KEY", "")
if gemini_key:
    print(f"✅ API Key configured: {gemini_key[:20]}...")
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Gemini works!'")
        print(f"✅ Status: WORKING")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Status: ERROR - {str(e)}")
else:
    print("❌ API Key: NOT CONFIGURED")

print()

# Test 3: HuggingFace
print("3️⃣ HUGGINGFACE")
print("-" * 80)
hf_key = os.getenv("HUGGINGFACE_API_KEY", "")
if hf_key:
    print(f"✅ API Key configured: {hf_key[:20]}...")
    try:
        from huggingface_hub import InferenceClient
        client = InferenceClient(token=hf_key)
        # Using a free model that's likely to work
        response = client.text_generation(
            "Say 'HuggingFace works!'",
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            max_new_tokens=50
        )
        print(f"✅ Status: WORKING")
        print(f"   Response: {response}")
    except Exception as e:
        error_msg = str(e)
        if "rate" in error_msg.lower() or "429" in error_msg:
            print(f"⚠️ Status: RATE LIMITED")
        elif "authorization" in error_msg.lower() or "401" in error_msg:
            print(f"❌ Status: INVALID API KEY")
        else:
            print(f"❌ Status: ERROR - {error_msg}")
else:
    print("❌ API Key: NOT CONFIGURED")
    print("   📝 Get free key at: https://huggingface.co/settings/tokens")
    print("   💡 Tip: Create a 'Read' token, then add to .env as HUGGINGFACE_API_KEY")

print()

# Test 4: Anthropic Claude
print("4️⃣ ANTHROPIC CLAUDE")
print("-" * 80)
anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
if anthropic_key:
    print(f"✅ API Key configured: {anthropic_key[:20]}...")
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=anthropic_key)
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'Claude works!'"}]
        )
        print(f"✅ Status: WORKING")
        print(f"   Response: {message.content[0].text}")
    except Exception as e:
        error_msg = str(e)
        if "rate" in error_msg.lower() or "429" in error_msg:
            print(f"⚠️ Status: RATE LIMITED")
        elif "authentication" in error_msg.lower() or "401" in error_msg:
            print(f"❌ Status: INVALID API KEY")
        else:
            print(f"❌ Status: ERROR - {error_msg}")
else:
    print("❌ API Key: NOT CONFIGURED")
    print("   📝 Get free key at: https://console.anthropic.com/")
    print("   💡 Tip: They offer $5 free credit, add to .env as ANTHROPIC_API_KEY")

print()
print("="*80)
print("📊 SUMMARY")
print("="*80)

# Count working providers
working = 0
if groq_key:
    working += 1
if gemini_key:
    working += 1
if hf_key:
    working += 1
if anthropic_key:
    working += 1

print(f"\n✅ Configured Providers: {working}/4")
print(f"\nFallback Chain: Groq → Gemini → HuggingFace → Anthropic")
print(f"\nRecommendation: Configure at least 2-3 providers for reliable fallback")

if working < 2:
    print(f"\n⚠️ WARNING: Only {working} provider(s) configured. Add more for better reliability!")

print()
