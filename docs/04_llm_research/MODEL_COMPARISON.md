# Free AI Models for Medical Triage - Comparison

## Current Model:
**llama-3.3-70b-versatile** via Groq
- Parameters: 70B
- Context: 32K tokens
- Speed: Very fast
- Medical capability: Good general reasoning

---

## Better Free Options for Medical Use:

### 1. **Llama 3.1 405B** (via Groq) ⭐ RECOMMENDED
```yaml
GROQ_MODEL=llama-3.1-405b-reasoning
```
**Pros:**
- ✅ 405B parameters (much more capable)
- ✅ Better reasoning for complex medical cases
- ✅ More accurate clinical decision-making
- ✅ Still free on Groq (with limits)
- ✅ Better at following structured prompts

**Cons:**
- ⚠️ Slower than 70B (but still fast on Groq)
- ⚠️ Lower rate limits

**Best for:** Complex medical reasoning, accurate specialty matching

---

### 2. **Llama 3.1 70B Versatile** (Current alternative)
```yaml
GROQ_MODEL=llama-3.1-70b-versatile
```
**Pros:**
- ✅ Latest stable 70B model
- ✅ Better than 3.3 for structured tasks
- ✅ Fast inference
- ✅ Good balance of speed/accuracy

---

### 3. **Mixtral 8x7B** via Groq
```yaml
GROQ_MODEL=mixtral-8x7b-32768
```
**Pros:**
- ✅ Excellent at following instructions
- ✅ Very fast
- ✅ Good for structured JSON output

**Cons:**
- ⚠️ Smaller than Llama models
- ⚠️ Less medical knowledge

---

### 4. **Google Gemini 1.5 Flash** (via API) 🌟 FREE & POWERFUL
```python
# Install: pip install google-generativeai
# Free quota: 15 requests/min, 1500/day
```

**Pros:**
- ✅ FREE with generous limits
- ✅ Excellent at medical reasoning
- ✅ 1M token context window
- ✅ Multimodal (can analyze images later)
- ✅ Strong at structured output
- ✅ Better safety features for medical use

**Cons:**
- ⚠️ Need separate API key (free from Google AI Studio)

---

### 5. **OpenAI GPT-4o-mini** (Low cost, not free)
```python
# ~$0.15 per 1M input tokens (very cheap)
```
**Pros:**
- ✅ Medical-grade reasoning
- ✅ Best accuracy for diagnosis
- ✅ Excellent at nuanced cases
- ✅ Strong safety guardrails

**Cons:**
- ⚠️ Not free (but very cheap)
- ⚠️ Need OpenAI credits

---

## Specialized Medical Models (Open Source):

### 6. **Med-PaLM 2** (Google) - Not publicly available
- Best medical AI model
- Not free/open

### 7. **BioMistral-7B** (HuggingFace)
```python
# Can run locally or via HF Inference API
```
**Pros:**
- ✅ Specifically trained on medical data
- ✅ Open source
- ✅ Free via HuggingFace

**Cons:**
- ⚠️ Only 7B parameters (less capable)
- ⚠️ Requires medical knowledge to prompt correctly

---

## RECOMMENDATION for Arogyamitra:

### Option 1: **Llama 3.1 405B** (Groq) - Best Free Choice
```bash
# In .env file:
GROQ_MODEL=llama-3.1-405b-reasoning
```

### Option 2: **Google Gemini 1.5 Flash** - Best Overall
```bash
# Get free API key from: https://aistudio.google.com/apikey
GEMINI_API_KEY=your_key_here
USE_GEMINI=true
```

### Option 3: **Hybrid Approach** (RECOMMENDED)
- Use **Gemini Flash** for triage (free, accurate)
- Fallback to **Llama 405B** if quota exceeded
- Best of both worlds

---

## Implementation Plan:

1. **Immediate:** Switch to Llama 3.1 405B (just change env var)
2. **Better:** Add Gemini Flash support (free, more accurate)
3. **Best:** Implement model fallback logic

---

## Medical Capability Ranking:

1. 🥇 **Gemini 1.5 Flash** - Best medical reasoning (FREE)
2. 🥈 **Llama 3.1 405B** - Excellent reasoning (FREE via Groq)
3. 🥉 **Llama 3.3 70B** - Good general purpose (Current)
4. **Mixtral 8x7B** - Fast but less medical knowledge
5. **BioMistral-7B** - Medical-specific but smaller

---

## Quick Switch to Better Model:

### Option A: Llama 405B (Easy - just update .env)
```bash
GROQ_MODEL=llama-3.1-405b-reasoning
```

### Option B: Gemini Flash (Best - need API key)
1. Get free key: https://aistudio.google.com/apikey
2. Add to .env:
   ```
   GEMINI_API_KEY=your_key_here
   USE_GEMINI=true
   ```
3. Install: `pip install google-generativeai`

---

## For Production:

Consider **Claude 3.5 Haiku** (Anthropic)
- Medical-grade safety
- Excellent reasoning
- ~$0.25 per 1M tokens (very cheap)
- Best for healthcare compliance

---

Would you like me to:
1. ✅ Switch to Llama 405B now (just .env change)
2. ✅ Add Gemini Flash support (best free option)
3. ✅ Implement model fallback (use both)
