# Arogyamitra Documentation

**Last Updated:** November 2, 2025

This documentation is organized into 5 main categories for easy navigation:

---

## 📂 Documentation Structure

### 01_setup/
**Getting started, deployment, and API configuration**

- `API_KEYS_SETUP.md` - How to obtain all required API keys
- `GET_GEMINI_KEY.md` - Google Gemini API key setup
- `GET_ANTHROPIC_KEY.md` - Anthropic Claude API key setup
- `DEPLOYMENT.md` - Quick deployment guide
- `DEPLOYMENT_GUIDE.md` - Detailed deployment instructions
- `LOCAL_TESTING_GUIDE.md` - Run and test bot locally
- `SETUP_COMPLETE.md` - Setup completion checklist

**Start here if:** You're setting up the bot for the first time

---

### 02_architecture/
**System design, protocols, and technical architecture**

- `VISUAL_ARCHITECTURE.md` - System architecture diagrams
- `MEDICAL_PROTOCOL.md` - Clinical SOAP protocol reference
- `REFACTORING_NOTES.md` - Code refactoring history

**Start here if:** You want to understand how the bot works internally

---

### 03_planning/
**Roadmaps, database schemas, and implementation plans**

- `VERSION_ROADMAP.md` - **Branch strategy & version timeline** ⭐
- `IMPLEMENTATION_SUMMARY.md` - MVP status and next steps
- `MVP_READINESS.md` - Active codebase, launch blockers, and free MVP path
- `DATABASE_PIPELINE.md` - Doctor database refresh workflow
- `FULL_PLATFORM_ROADMAP.md` - 6-phase implementation plan
- `DATA_SCHEMA.md` - Complete database design
- `DATA_COLLECTION_TEMPLATE.md` - Form for data entry team
- `ISSUE_ANALYSIS.md` - Bug analysis and solutions
- `ZERO_COST_MVP.md` - Free tier operation guide

**Start here if:** You're planning features or understanding the roadmap

---

### 04_llm_research/
**LLM providers, comparisons, and rate limit solutions**

- `FREE_LLM_OPTIONS.md` - Research on free LLM providers
- `FREE_LLM_RESEARCH.md` - Detailed provider comparison
- `FREE_LLM_SETUP_COMPLETE.md` - Multi-provider setup guide
- `MODEL_COMPARISON.md` - LLM performance comparisons
- `RATE_LIMIT_SOLUTION.md` - Rate limit handling strategies

**Start here if:** You're working on LLM integration or troubleshooting rate limits

---

### 05_testing/
**Test results, validation, and quality assurance**

- `TEST_RESULTS.md` - Comprehensive test execution results
- `README-bot.md` - Bot testing documentation

**Start here if:** You're testing the bot or validating changes

---

## 🔍 Quick Find

### I want to...

**Deploy the bot**
→ Start with `01_setup/DEPLOYMENT_GUIDE.md`

**Understand the version strategy**
→ Read `03_planning/VERSION_ROADMAP.md` ⭐

**Add a new LLM provider**
→ Check `04_llm_research/FREE_LLM_OPTIONS.md`

**Fix rate limit issues**
→ See `04_llm_research/RATE_LIMIT_SOLUTION.md`

**Plan database changes**
→ Review `03_planning/DATA_SCHEMA.md`

**Test the bot**
→ Follow `01_setup/LOCAL_TESTING_GUIDE.md`

**Get API keys**
→ Use `01_setup/API_KEYS_SETUP.md`

**Understand the architecture**
→ Read `02_architecture/VISUAL_ARCHITECTURE.md`

---

## 📊 Current Branch Status

| Branch | Purpose | Documentation Focus |
|--------|---------|---------------------|
| `main` | Production stable | Deployment guides |
| `1_MVP_base` | Stable baseline | MVP summary |
| `dev` | Active development | All docs |

See `03_planning/VERSION_ROADMAP.md` for complete branch strategy.

---

## 🚀 Getting Started (Quick Path)

1. **Setup Environment**
   - Read `01_setup/API_KEYS_SETUP.md`
   - Follow `01_setup/LOCAL_TESTING_GUIDE.md`

2. **Understand the Bot**
   - Review `03_planning/IMPLEMENTATION_SUMMARY.md`
   - Check `02_architecture/MEDICAL_PROTOCOL.md`

3. **Deploy**
   - Use `01_setup/DEPLOYMENT_GUIDE.md`
   - Verify with `01_setup/SETUP_COMPLETE.md`

4. **Plan Next Features**
   - Study `03_planning/VERSION_ROADMAP.md`
   - Review `03_planning/FULL_PLATFORM_ROADMAP.md`

---

## 📝 Contributing to Documentation

When adding new documentation:

1. **Determine category:**
   - Setup/deployment → `01_setup/`
   - Architecture/design → `02_architecture/`
   - Planning/roadmaps → `03_planning/`
   - LLM research → `04_llm_research/`
   - Testing/validation → `05_testing/`

2. **Name clearly:** `WHAT_IT_COVERS.md`

3. **Update this README:** Add entry in appropriate section

4. **Keep consistent:** Use markdown formatting, add date/status

---

## 💡 Documentation Standards

All documentation should include:
- **Last Updated:** Date
- **Status:** (Complete/In Progress/Planned)
- **Purpose:** One-line description
- Clear sections with headers
- Code examples when relevant
- Links to related docs

---

**Questions?** Check the appropriate category folder or start with `03_planning/VERSION_ROADMAP.md` for the big picture.
