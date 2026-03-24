# API Keys Setup Guide

## Currently Configured ✅

1. **Groq** - WORKING ✅
   - Fast, reliable, good free tier
   - Rate limit: 100K tokens/day (currently hit, will reset)

2. **Gemini** - WORKING ✅
   - Google's LLM, generous free tier
   - Successfully tested and working as fallback

## Additional Providers (Optional)

### 3. HuggingFace (FREE)
Get your free API key:
1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Select "Read" access
4. Copy the token
5. Add to `.env`:
   ```
   HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
   ```

**Free Tier**: Unlimited requests with rate limiting

### 4. Anthropic Claude (FREE $5 CREDIT)
Get your API key:
1. Go to: https://console.anthropic.com/
2. Sign up (they give $5 free credit)
3. Go to API Keys section
4. Create new key
5. Add to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
   ```

**Free Tier**: $5 credit (~500K tokens)

## Fallback Chain

```
Groq (Primary) 
  ↓ (if rate limited)
Gemini (Secondary) ✅ ACTIVE
  ↓ (if fails)
HuggingFace (Tertiary) 
  ↓ (if fails)
Anthropic (Final)
```

## Current Status

- **Working Providers**: 2/4 (Groq + Gemini)
- **Fallback**: ✅ Functional
- **Recommendation**: You have sufficient coverage with Groq + Gemini for production use

## Testing

Run provider tests:
```bash
python test_providers.py
```

Run comprehensive bot tests:
```bash
python test_comprehensive.py
```
