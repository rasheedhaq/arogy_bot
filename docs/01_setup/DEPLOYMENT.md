# 🚀 Deployment Guide - ARM_MVP0 (Free Hosting)

This guide helps you deploy Arogyamitra Bot to free hosting platforms so it runs 24/7 even when your laptop is off.

---

## 🎯 Best Free Options for ARM_MVP0

### 🏆 Option 1: Railway.app (RECOMMENDED)
**Perfect for Telegram bots**

#### ✅ Pros:
- 500 hours/month FREE ($5 credit)
- Auto-deploy from GitHub
- Environment variables support
- No credit card required initially
- Easy setup

#### 📝 Setup Steps:

1. **Sign up at Railway.app**
   - Go to: https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your `arogy_bot` repository

3. **Add Environment Variables**
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   GROQ_API_KEY=your_groq_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   DOCTORS_DB_PATH=data/doctors_enhanced.csv
   USE_GEMINI=false
   DEBUG=false
   ENVIRONMENT=production
   ```

4. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

5. **Deploy**
   - Railway auto-deploys on git push
   - Check logs for "Bot is running"

#### 💰 Cost:
- **FREE for 500 hours/month** (~20 days)
- After free tier: $5/month

---

### 🥈 Option 2: Render.com
**Good alternative**

#### ✅ Pros:
- FREE tier available
- Auto-sleep after 15 min inactivity (wakes on request)
- Easy GitHub integration

#### ⚠️ Cons:
- Sleeps when inactive (not ideal for 24/7 bot)
- Need paid plan ($7/month) for always-on

#### 📝 Setup Steps:

1. **Sign up at Render.com**
   - Go to: https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repo

3. **Configure Service**
   ```
   Name: arogyamitra-bot
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   ```

4. **Add Environment Variables**
   - Same as Railway (see above)

5. **Deploy**
   - Click "Create Web Service"

#### 💰 Cost:
- **FREE** (with auto-sleep)
- Always-on: $7/month

---

### 🥉 Option 3: Fly.io
**Best performance**

#### ✅ Pros:
- 3 VMs FREE
- Always-on
- Good uptime

#### 📝 Setup Steps:

1. **Install Fly CLI**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login & Initialize**
   ```bash
   fly auth login
   cd arogy_bot
   fly launch
   ```

3. **Configure fly.toml** (auto-generated)
   ```toml
   app = "arogyamitra-bot"
   
   [build]
   
   [env]
     GROQ_MODEL = "llama-3.3-70b-versatile"
     DOCTORS_DB_PATH = "data/doctors_enhanced.csv"
   ```

4. **Set Secrets**
   ```bash
   fly secrets set TELEGRAM_BOT_TOKEN=your_token_here
   fly secrets set GROQ_API_KEY=your_groq_key_here
   ```

5. **Deploy**
   ```bash
   fly deploy
   ```

#### 💰 Cost:
- **FREE for 3 VMs**
- After: ~$2/month per VM

---

### Option 4: PythonAnywhere
**Simplest but limited**

#### ✅ Pros:
- Easy Python setup
- No Docker needed

#### ⚠️ Cons:
- Free tier: only web apps (no always-on scripts)
- Need $5/month for always-on

#### 📝 Setup Steps:

1. **Sign up**
   - https://www.pythonanywhere.com

2. **Upload Code**
   - Use Git or upload files

3. **Create Always-On Task** (Paid only)
   - Task: `python /home/username/arogy_bot/main.py`

#### 💰 Cost:
- **FREE** (web apps only)
- Always-on: $5/month

---

## 🔧 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] `.gitignore` excludes `.env` and sensitive files
- [ ] `.env.example` is committed (template)
- [ ] Real `.env` is NOT committed
- [ ] `doctors_sample.csv` committed (dummy data)
- [ ] Real `doctors_enhanced.csv` excluded
- [ ] `requirements.txt` updated
- [ ] Bot tested locally
- [ ] README.md updated with your info

---

## 📦 Required Files for Deployment

### Must Have:
1. **`requirements.txt`** - Dependencies
2. **`main.py`** - Entry point
3. **`Procfile`** (optional, for some platforms)
4. **`.env.example`** - Template for secrets
5. **`data/doctors_sample.csv`** - Sample data

### Must NOT Have (in git):
1. ❌ `.env` - Contains secrets
2. ❌ `doctors_enhanced.csv` - Real doctor data
3. ❌ `__pycache__/` - Python cache
4. ❌ API keys in any file

---

## 🚀 Deployment Commands

### Railway.app
```bash
# Auto-deploys on git push
git add .
git commit -m "Deploy ARM_MVP0"
git push origin main
```

### Render.com
```bash
# Auto-deploys on git push
git push origin main
# Check dashboard for deployment status
```

### Fly.io
```bash
fly deploy
fly logs
fly status
```

---

## 🔍 Monitoring & Logs

### Railway:
- Dashboard → Your Project → Logs
- Real-time logs

### Render:
- Dashboard → Your Service → Logs
- Logs tab

### Fly.io:
```bash
fly logs
fly status
```

---

## 🛠️ Troubleshooting

### Bot not starting?
1. Check logs for errors
2. Verify environment variables set correctly
3. Ensure `TELEGRAM_BOT_TOKEN` is valid
4. Test Groq API key

### "Module not found" error?
- Check `requirements.txt` includes all dependencies
- Re-deploy after updating requirements

### Bot sleeps on Render?
- Free tier sleeps after inactivity
- Upgrade to paid ($7/month) for always-on
- Or use Railway/Fly.io instead

### API rate limits?
- Groq free tier: 14,400 requests/day
- Should be sufficient for MVP
- Monitor usage in Groq dashboard

---

## 💡 Tips for Free Hosting

1. **Use Railway for MVP0** - Best free option
2. **Monitor usage** - Stay within free limits
3. **Set up alerts** - Get notified if bot goes down
4. **Backup data** - Keep doctor data backed up
5. **Update regularly** - Push fixes via git

---

## 📊 Cost Comparison

| Platform | Free Tier | Always-On | Auto-Deploy | Best For |
|----------|-----------|-----------|-------------|----------|
| **Railway** | 500 hrs/mo | ✅ Yes | ✅ Yes | MVP0 |
| **Render** | Yes (sleeps) | ❌ $7/mo | ✅ Yes | Testing |
| **Fly.io** | 3 VMs | ✅ Yes | ✅ Yes | Production |
| **PythonAnywhere** | Web only | ❌ $5/mo | ❌ Manual | Simple |

---

## 🎯 Recommended: Railway.app

**For ARM_MVP0, use Railway because:**
- ✅ 500 hours FREE = ~20 days runtime
- ✅ Auto-deploy from GitHub
- ✅ Environment variables
- ✅ Good logs
- ✅ No credit card needed initially
- ✅ Easy to scale later

**After 500 hours:** Either:
1. Create new account (reset free tier) 
2. Pay $5/month (worth it)
3. Switch to Fly.io (3 VMs free)

---

## 📝 Next Steps After Deployment

1. **Test the bot** on Telegram
2. **Monitor logs** for errors
3. **Set up monitoring** (UptimeRobot - free)
4. **Share with users**
5. **Collect feedback**
6. **Plan Phase 2** (real doctor data)

---

## 🆘 Support

**Having issues?**
- Check platform documentation
- Review logs carefully
- Test locally first
- Ask in GitHub Discussions

---

**Ready to deploy? Let's start with Railway.app! 🚀**
