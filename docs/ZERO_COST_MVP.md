# 💰 Zero-Cost MVP Architecture

## ✅ **100% FREE Services Used**

### 1. **Groq API** (LLM Inference)
- **Model:** llama-3.3-70b-versatile
- **Cost:** FREE
- **Limits:** 
  - 30 requests/minute
  - 14,400 requests/day
  - Plenty for MVP testing!
- **API Key:** Get free at https://console.groq.com

### 2. **Telegram Bot API** 
- **Cost:** FREE forever
- **Limits:** None for basic messaging
- **Your Bot:** @arogyamitr_bot

### 3. **Python + Conda**
- **Cost:** FREE
- **Environment:** arogyamitra_env (Python 3.13)

---

## 📊 **What Your MVP Does (Zero Cost)**

1. **Receives patient messages** on Telegram
2. **Asks 8 structured questions:**
   - Chief complaint
   - Duration
   - Severity (1-10)
   - Associated symptoms
   - Age
   - Location (pincode)
   - Chronic conditions
   - Current medications

3. **Uses AI to analyze** symptoms via Groq's free API
4. **Matches with doctors** from CSV database (19 doctors)
5. **Sends 2 doctor recommendations** with:
   - Name & specialty
   - Clinic name & address
   - Match score

---

## 💡 **Free Tier Limits**

| Service | Free Limit | MVP Impact |
|---------|-----------|------------|
| Groq API | 30 req/min | ✅ Good for testing |
| Telegram | Unlimited | ✅ Perfect |
| Database | CSV file | ✅ Free forever |

---

## 🚀 **Cost Scaling (When You Grow)**

**Current (0-100 users/day):** $0/month

**Future Options:**
- Keep Groq free tier (14,400 daily = ~600 users/day)
- Add PostgreSQL free tier (Supabase/Neon)
- Gemini API also has free tier as backup

---

## 🎯 **MVP Ready!**

Your bot is 100% free and works right now at:
👉 https://t.me/arogyamitr_bot

Test it with: "headache" or "fever"
