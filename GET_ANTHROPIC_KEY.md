# 🚀 Get Anthropic Claude API Key (2 minutes)

## Current Status
✅ HuggingFace: Already configured! (`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`)
⏸️ Anthropic: Need to add

## Steps to Get Anthropic API Key

### 1. Sign Up (FREE $5 credit)
Visit: **https://console.anthropic.com/signup**

### 2. Verify Email
- Check your email inbox
- Click verification link

### 3. Create API Key
- Go to: https://console.anthropic.com/settings/keys
- Click **"Create Key"**
- Name it: `arogyamitra-bot`
- Copy the key (starts with `sk-ant-...`)

### 4. Add to .env File
Open `.env` and replace this line:
```env
ANTHROPIC_API_KEY=
```

With:
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 5. Test All Providers
```bash
conda activate arogyamitra_env
python test_providers.py
```

Expected output:
```
✅ Configured Providers: 4/4
Fallback Chain: Groq → Gemini → HuggingFace → Anthropic
```

## Anthropic Free Tier Details
- **Free Credit**: $5 (enough for ~10,000 requests)
- **Model**: claude-3-haiku-20240307 (fast, smart)
- **Rate Limit**: 5 requests/minute on free tier
- **Perfect for**: Final fallback provider

## After Setup
Once you add the Anthropic key, you'll have **4 providers**:
1. Groq (fastest, 100K tokens/day)
2. Gemini (10 req/min)
3. HuggingFace (generous limits) ✅
4. Anthropic ($5 credit)

This means you can run comprehensive tests 24/7 without hitting rate limits!
