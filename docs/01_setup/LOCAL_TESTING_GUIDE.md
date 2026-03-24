# 🧪 LOCAL TESTING GUIDE

## Bot Status
✅ **Bot is RUNNING locally!**
- Terminal is active with bot polling for messages
- Providers: Groq + HuggingFace (Gemini disabled due to package issue)
- Database: 19 doctors loaded

## 📱 How to Test on Telegram

### Step 1: Find Your Bot
1. Open **Telegram** on your phone or desktop
2. Search for your bot by username (check @BotFather for the username)
   - Or use this link format: `t.me/YOUR_BOT_USERNAME`

### Step 2: Start the Bot
1. Click **"START"** or send `/start`
2. Expected response: Welcome message with instructions

### Step 3: Test Basic Conversation
**Test Case 1: Simple Medical Query**
```
You: I have fever since 2 days
Bot: [Should ask follow-up questions like "How high is your fever?"]
```

**Test Case 2: Provide More Details**
```
You: 102F, also have headache and body pain
Bot: [Should continue asking relevant questions]
You: 2 days, getting worse
Bot: [Should eventually recommend a doctor]
```

**Test Case 3: Edge Case - Gibberish**
```
You: ggg,ggg,hhh
Bot: [Should handle gracefully, ask what's wrong]
```

**Test Case 4: Emergency**
```
You: severe chest pain and difficulty breathing
Bot: [Should recognize urgency and recommend appropriate specialist]
```

**Test Case 5: Complete Flow**
```
You: /start
Bot: Welcome message
You: tooth pain
Bot: Follow-up questions
You: severe pain, swollen gums, 3 days
Bot: [Should recommend dentist/ENT specialist with details]
```

## 🔍 What to Check

### ✅ Bot Responds Quickly
- Response time should be < 3 seconds
- No timeout errors

### ✅ Intelligent Conversation
- Bot asks relevant follow-up questions
- Doesn't jump to recommendation too quickly
- Understands medical context

### ✅ Doctor Recommendations
- Bot provides doctor name, specialty, location
- Recommendations are relevant to symptoms
- Contact details are included

### ✅ Edge Case Handling
- Gibberish input handled gracefully
- Empty messages don't crash the bot
- "no" responses are managed

### ✅ Error Handling
- If Groq rate limit hits, should fallback to HuggingFace
- No unhandled exceptions visible to user

## 📊 Monitor Terminal Output

While testing, watch the terminal for:
```
✅ Normal logs:
- User messages
- Bot responses
- Doctor recommendations

⚠️ Warnings to watch for:
- "⚠️ Groq rate limit hit, trying next provider..."
- This is NORMAL and expected

❌ Errors to report:
- "❌ All LLM providers failed"
- Crash/traceback messages
- "No response from LLM"
```

## 🎯 Test Scenarios

### Scenario 1: General Health Issue
```
Symptom: "feeling sick with cold and cough"
Expected Doctor: General Physician
```

### Scenario 2: Women's Health
```
Symptom: "irregular periods and pelvic pain"
Expected Doctor: Gynaecologist
```

### Scenario 3: Child Health
```
Symptom: "my baby has high fever and rash"
Expected Doctor: Pediatrician
```

### Scenario 4: Heart Issue
```
Symptom: "chest pain and palpitations"
Expected Doctor: Cardiologist
```

### Scenario 5: Skin Problem
```
Symptom: "skin rash and itching"
Expected Doctor: Dermatologist
```

## 🛑 How to Stop the Bot

When done testing:
1. Go to the terminal running the bot
2. Press `Ctrl+C` to stop
3. Bot will shut down gracefully

## 📝 Things to Note During Testing

**Performance:**
- [ ] Response time
- [ ] Conversation flow quality
- [ ] Doctor recommendation accuracy

**Issues Found:**
- [ ] Any crashes?
- [ ] Confusing responses?
- [ ] Wrong doctor recommendations?
- [ ] Rate limit problems?

**User Experience:**
- [ ] Easy to use?
- [ ] Clear instructions?
- [ ] Helpful responses?

## 🚀 After Testing

Once local testing is successful:
1. Stop the bot (Ctrl+C)
2. Fix any issues found
3. Re-enable Gemini (fix package issue)
4. Deploy to Railway for 24/7 operation

---

**Current Status:** 
✅ Bot running on: `http://localhost` (Telegram polling)
✅ Providers: Groq (primary) → HuggingFace (fallback)
✅ Database: 19 doctors loaded
✅ Ready for testing!

**Start testing now on Telegram!** 📱
