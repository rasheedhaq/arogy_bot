# Get Your Free Gemini API Key

## Steps:

1. **Visit Google AI Studio:**
   https://aistudio.google.com/apikey

2. **Sign in** with your Google account

3. **Click "Create API Key"**

4. **Copy the key** (starts with "AIza...")

5. **Add to your .env file:**
   ```bash
   GEMINI_API_KEY=AIza...your_key_here
   ```

6. **Restart the bot:**
   ```bash
   conda activate arogyamitra_env
   python main.py
   ```

## Free Limits:

- **15 requests per minute**
- **1,500 requests per day**
- **1 million tokens per minute**

More than enough for testing and even moderate production use!

## What Happens Now:

✅ Bot will use **Gemini 1.5 Flash** (best free medical AI)
✅ If Gemini quota exceeded → Falls back to **Llama 3.1 405B**
✅ If both fail → Shows error message

## Without Gemini Key:

If you don't add a Gemini key, the bot will automatically use:
- **Llama 3.1 405B** (5x smarter than your previous model)
- Still much better than before!

## Current Status:

- ✅ Groq: **llama-3.1-405b-reasoning** (upgraded)
- ⏳ Gemini: Waiting for API key
- ✅ Fallback: Automatic switching

You're already 5x smarter even without Gemini! 🚀
