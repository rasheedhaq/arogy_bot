# 🚀 DEPLOYMENT GUIDE - Railway

## Pre-Deployment Checklist ✅

- [x] Bot functionality tested
- [x] Multi-provider LLM fallback implemented (Groq → Gemini → HuggingFace)
- [x] All dependencies listed in requirements.txt
- [x] Environment variables configured in .env
- [x] Doctor database ready (data/doctors_clean.csv)
- [x] Error handling and graceful degradation implemented

## 📋 Railway Environment Variables

Copy these environment variables to Railway:

```env
# Required - Telegram Bot
TELEGRAM_BOT_TOKEN=8421218551:AAE_SScfAIo67AiIOrjoKJOMbJZts3TSDt0

# Required - Primary LLM Provider
GROQ_API_KEY=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
GROQ_MODEL=llama-3.3-70b-versatile

# Required - Fallback Provider #1
GEMINI_API_KEY=AIzaSyCDxyc5aFyjbqIwZNYeCG80z63I6My_Nao
USE_GEMINI=true
GEMINI_MODEL=gemini-2.5-flash

# Optional - Fallback Provider #2
HUGGINGFACE_API_KEY=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
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.2

# Optional - Fallback Provider #3 (if you have it)
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Application Settings
BASE_URL=http://localhost:8000
DEBUG=false
ENVIRONMENT=production
DOCTORS_DB_PATH=data/doctors_clean.csv

# WhatsApp (future use)
WHATSAPP_VERIFY_TOKEN=verify-me
WHATSAPP_TOKEN=
```

## 🚂 Railway Deployment Steps

### 1. Connect Repository
1. Go to: https://railway.app/
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose: `rasheedhaq/arogy_bot`
5. Select branch: `dev`

### 2. Configure Environment Variables
1. In Railway dashboard, go to your project
2. Click "Variables" tab
3. Add all environment variables from above (copy-paste each)
4. **Important**: Set `DEBUG=false` for production
5. **Important**: Set `ENVIRONMENT=production`

### 3. Configure Start Command
Railway should auto-detect Python, but if needed:
- **Start Command**: `python main.py`
- **Build Command**: `pip install -r requirements.txt`

### 4. Deploy
1. Railway will auto-deploy on git push
2. Monitor logs in Railway dashboard
3. Look for: `"Bot is running. Press Ctrl+C to stop."`

## 🧪 Post-Deployment Testing

### Test the deployed bot:
1. Open Telegram
2. Search for your bot: `@your_bot_name`
3. Send: `/start`
4. Expected: Welcome message with instructions
5. Send: "I have fever"
6. Expected: Bot asks follow-up questions
7. Complete conversation
8. Expected: Bot recommends appropriate doctor

### Monitor logs:
```bash
railway logs
```

Look for:
- ✅ `LLM Providers initialized (2-3)`
- ✅ `Loaded X doctors from database`
- ✅ `Bot is running`
- ⚠️ Check for any rate limit warnings
- ❌ Check for any error messages

## 🔧 Troubleshooting

### Issue: Bot not responding
**Solution**: Check Railway logs for errors
```bash
railway logs --follow
```

### Issue: "All LLM providers failed"
**Solution**: 
1. Check API keys are correct in Railway variables
2. Verify Groq/Gemini have available quota
3. Add Anthropic key for additional fallback

### Issue: "Doctor not found" errors
**Solution**: Verify `data/doctors_clean.csv` exists in repository

### Issue: Import errors
**Solution**: Check `requirements.txt` has all dependencies
```bash
railway run pip list
```

## 📊 Monitoring Production

### Key Metrics to Watch:
1. **Response Time**: Should be < 3 seconds
2. **Error Rate**: Should be < 1%
3. **Provider Fallback Rate**: How often Gemini is used vs Groq
4. **User Satisfaction**: Successful doctor recommendations

### Log Analysis:
Look for patterns in logs:
- `⚠️ Groq rate limit hit` → Common, expected
- `✅ Gemini` → Fallback working correctly
- `❌ All LLM providers failed` → Critical issue

## 🎯 Success Criteria

✅ Bot responds to `/start`
✅ Bot handles medical queries intelligently
✅ Fallback mechanism works (Groq → Gemini)
✅ Doctor recommendations are accurate
✅ Edge cases handled gracefully (gibberish, empty input)
✅ No crashes or unhandled exceptions

## 📈 Next Steps After Deployment

1. **Monitor first 24 hours closely**
2. **Collect user feedback**
3. **Add Anthropic key** for stronger fallback ($5 free credit)
4. **Set up alerts** for critical errors
5. **Track usage patterns** to optimize performance

## 🚨 Emergency Rollback

If issues occur:
1. Go to Railway dashboard
2. Click "Deployments"
3. Find last working deployment
4. Click "Redeploy"

Or use git:
```bash
git revert HEAD
git push origin dev
```

---

## ✅ DEPLOYMENT READY!

The bot is tested and ready for production deployment. The multi-provider fallback ensures reliability even during rate limits.

**Estimated Downtime**: 0 minutes (Railway handles zero-downtime deploys)
**Estimated Setup Time**: 5-10 minutes
**Production Readiness**: ✅ READY
