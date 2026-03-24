# Arogyamitra Bot - Version Roadmap & Branch Strategy

**Last Updated:** November 2, 2025  
**Current Status:** Development Phase - Intelligent Conversation Flow

---

## Branch Strategy

Each branch represents a **stable, deployable version** with specific features frozen. This allows:
- ✅ Easy rollback to stable versions
- ✅ Feature experimentation without breaking production
- ✅ Clear milestone tracking
- ✅ Parallel development paths

---

## Version Branches

### `main` - Production Stable
**Purpose:** Only production-ready, battle-tested code  
**Deployment:** Railway production instance  
**Update Frequency:** After thorough testing on dev  
**Protection:** Protected branch, requires PR approval

---

### `1_MVP_base` - Foundation (Current Stable Checkpoint)
**Status:** ✅ Stable - Ready for baseline deployment  
**Created:** November 2, 2025

**Features:**
- ✅ Telegram bot with /start command
- ✅ LLM-driven conversation (Groq primary, 4 fallback providers)
- ✅ Patient demographics collection (Name, Age, Sex, Mobile, Address)
- ✅ Medical symptom gathering (Chief complaint, duration, severity)
- ✅ Emergency detection and routing
- ✅ Doctor matching from CSV database (19 doctors)
- ✅ Doctor recommendation with formatted cards
- ✅ Rate limit persistence across restarts

**Database:** `data/doctors_clean.csv` (19 doctors)

**LLM Providers:**
1. Groq (llama-3.3-70b-versatile) - Primary
2. Deepseek (deepseek-chat)
3. OpenRouter (gemini-2.0-flash-exp:free)
4. Gemini (gemini-2.5-flash)
5. HuggingFace (Mistral-7B)

**Limitations:**
- No multi-field extraction intelligence
- Basic sequential question flow
- CSV-based doctor database only
- No appointment booking
- No payment integration

**Use Case:** Baseline for comparison, fallback stable version

---

### `dev` - Active Development (Current)
**Status:** 🚧 Active Development  
**Last Updated:** November 2, 2025

**Recent Enhancements:**
- ✅ Fixed infinite greeting loop bug
- ✅ Added multi-field extraction intelligence
- ✅ Improved LLM prompt for smarter information gathering
- ✅ Organized documentation into categorized folders
- 🚧 Testing intelligent response handling

**Testing Focus:**
- Multi-field extraction (e.g., "rasheed male 33" extracts all three)
- Skip already-collected fields
- Natural conversation flow
- Emergency detection at any point

**Next Steps:**
1. Test intelligent extraction thoroughly
2. Merge to `1_MVP_base` once stable
3. Branch to `2_MVP_enhanced` for next features

---

### `2_MVP_enhanced` - Intelligent Conversation (Planned)
**Status:** 📋 Planned - Not yet created  
**Target Date:** November 5-10, 2025

**New Features:**
- ✅ Multi-field extraction from single response
- ✅ Context-aware question skipping
- ✅ Personalized conversation using patient name
- ✅ Smarter specialty matching
- ✅ Conversation history persistence
- ✅ Better error recovery

**Database Upgrade:**
- Add `doctors_enhanced.csv` with extended fields
- Include: Mobile, Email, Qualifications, Experience, Languages
- Implement exclude_keywords for precise matching

**LLM Enhancements:**
- Better prompt engineering for extraction
- Few-shot examples in system prompt
- Fallback graceful degradation

**Use Case:** Production-ready intelligent medical assistant

---

### `3_appointment_booking` - Booking System (Planned)
**Status:** 📋 Planned  
**Target Date:** November 15-25, 2025

**New Features:**
- ✅ Doctor availability calendar (days/hours)
- ✅ Appointment slot selection
- ✅ Booking confirmation via SMS/Email
- ✅ Patient appointment history
- ✅ Appointment cancellation/rescheduling

**Database Upgrade:**
```sql
doctors table:
+ consultation_days (JSON: ["Mon", "Tue", "Wed"])
+ consultation_hours_start
+ consultation_hours_end
+ appointment_required (boolean)
+ online_consult_available (boolean)

appointments table (new):
- appointment_id
- patient_id
- doctor_id
- appointment_date
- appointment_time
- status (pending/confirmed/cancelled)
- consultation_type (in-person/online)
```

**External Integrations:**
- Twilio/AWS SNS for SMS notifications
- SendGrid/AWS SES for email confirmations
- Google Calendar API for doctor schedules

**Use Case:** Full appointment management system

---

### `4_location_maps` - Proximity & Maps (Planned)
**Status:** 📋 Planned  
**Target Date:** December 1-10, 2025

**New Features:**
- ✅ Patient location collection (pincode/GPS)
- ✅ Distance calculation from patient to doctor
- ✅ Sort doctors by proximity
- ✅ Google Maps integration for directions
- ✅ Clinic images and reviews

**Database Upgrade:**
```sql
doctors table:
+ latitude
+ longitude
+ clinic_images (JSON array of URLs)
+ average_rating (1-5)
+ total_reviews

patient_locations table (new):
- patient_id
- latitude
- longitude
- pincode
- city
```

**External Integrations:**
- Google Maps API (geocoding, distance matrix)
- Google Places API (clinic photos, reviews)
- OpenStreetMap (free alternative)

**Use Case:** Location-aware doctor recommendations

---

### `5_payments` - Payment Gateway (Planned)
**Status:** 📋 Planned  
**Target Date:** December 15-30, 2025

**New Features:**
- ✅ Consultation fee display
- ✅ Online payment (Razorpay/Stripe)
- ✅ Payment confirmation
- ✅ Invoice generation (PDF)
- ✅ Refund handling
- ✅ Payment history

**Database Upgrade:**
```sql
doctors table:
+ consultation_fee
+ online_consultation_fee
+ payment_gateway_id

payments table (new):
- payment_id
- appointment_id
- patient_id
- amount
- payment_method
- payment_status
- transaction_id
- invoice_url
- refund_status
```

**External Integrations:**
- Razorpay Payment Gateway (recommended for India)
- Stripe (international)
- PDF generation library (ReportLab/WeasyPrint)

**Use Case:** Complete transactional system

---

### `6_full_platform` - Reviews & Analytics (Planned)
**Status:** 📋 Planned  
**Target Date:** January 2026

**New Features:**
- ✅ Patient reviews & ratings
- ✅ Doctor response to reviews
- ✅ Follow-up appointment reminders
- ✅ Admin analytics dashboard
- ✅ Doctor performance metrics
- ✅ Patient satisfaction tracking

**Database Upgrade:**
```sql
reviews table (new):
- review_id
- patient_id
- doctor_id
- appointment_id
- rating (1-5)
- comment
- doctor_response
- created_at

analytics table (new):
- metric_id
- metric_type (bookings/revenue/satisfaction)
- date
- value
- doctor_id (optional)
```

**Admin Features:**
- Dashboard with charts (Chart.js/Plotly)
- Revenue tracking
- Popular specialties
- Patient demographics
- Doctor performance rankings

**Use Case:** Complete healthcare platform with insights

---

## Migration Path

### Current State → 1_MVP_base
```bash
# Save current dev state
git checkout dev
git pull

# Create stable baseline branch
git checkout -b 1_MVP_base
git push -u origin 1_MVP_base

# Continue development on dev
git checkout dev
```

### 1_MVP_base → 2_MVP_enhanced
```bash
# After thorough testing of intelligent extraction
git checkout dev
git pull

# Create enhanced branch
git checkout -b 2_MVP_enhanced
git push -u origin 2_MVP_enhanced

# Merge to main after validation
git checkout main
git merge 2_MVP_enhanced
git push
```

---

## Version Naming Convention

**Branch Name Format:** `{number}_{feature_name}`

Examples:
- `1_MVP_base` - First stable version
- `2_MVP_enhanced` - Second iteration with enhancements
- `3_appointment_booking` - Major feature addition
- `4_location_maps` - Another major feature

**Benefits:**
- Number prefix for sorting
- Descriptive feature name
- Easy to understand timeline

---

## Database Evolution

### Phase 1: CSV (Current - 1_MVP_base)
```
data/doctors_clean.csv
- Simple, easy to edit
- No complex setup
- Works for <100 doctors
```

### Phase 2: Enhanced CSV (2_MVP_enhanced)
```
data/doctors_enhanced.csv
+ More fields (mobile, email, qualifications)
+ Better keyword mapping
+ exclude_keywords for precision
```

### Phase 3: SQLite (3_appointment_booking)
```
data/arogyamitra.db
- appointments table
- patient_history table
- Supports relational queries
- Still portable (single file)
```

### Phase 4: PostgreSQL (5_payments onwards)
```
Production Database
- Cloud-hosted (Railway/Heroku)
- Transactions support
- Better concurrency
- Backup automation
```

---

## Testing Strategy Per Branch

### 1_MVP_base Testing
- [ ] /start command works
- [ ] Collects all 5 demographics
- [ ] Asks medical questions
- [ ] Recommends correct specialty
- [ ] Shows 2 relevant doctors
- [ ] Emergency detection works

### 2_MVP_enhanced Testing
- [ ] "rasheed male 33" extracts 3 fields ✅
- [ ] Skips already-collected fields ✅
- [ ] Uses patient name in questions ✅
- [ ] Handles typos gracefully
- [ ] Multi-provider fallback works
- [ ] Conversation persists across restarts

### 3_appointment_booking Testing
- [ ] Shows available time slots
- [ ] Books appointment successfully
- [ ] Sends SMS confirmation
- [ ] Email confirmation received
- [ ] Can reschedule appointment
- [ ] Can cancel appointment

### 4_location_maps Testing
- [ ] Gets patient location
- [ ] Calculates distances correctly
- [ ] Sorts doctors by proximity
- [ ] Google Maps link works
- [ ] Shows clinic on map

### 5_payments Testing
- [ ] Displays consultation fee
- [ ] Payment gateway loads
- [ ] Payment succeeds
- [ ] Invoice generated
- [ ] Refund processes correctly

---

## Deployment Per Branch

### 1_MVP_base Deployment
```yaml
Platform: Railway (free tier)
Database: CSV in repo
LLM: Groq (free)
Estimated Cost: $0/month
Users Supported: 100-500/day
```

### 2_MVP_enhanced Deployment
```yaml
Platform: Railway (hobby tier)
Database: Enhanced CSV
LLM: Groq + 3 fallbacks
Estimated Cost: $5-10/month
Users Supported: 1000-2000/day
```

### 3_appointment_booking Deployment
```yaml
Platform: Railway (starter)
Database: SQLite → PostgreSQL
Notifications: Twilio ($20/month)
Estimated Cost: $25-40/month
Users Supported: 5000-10000/day
```

### 5_payments Deployment
```yaml
Platform: Railway (pro) or AWS
Database: PostgreSQL (managed)
Payment: Razorpay (2% per transaction)
Estimated Cost: $100-200/month + transaction fees
Users Supported: 50,000+/day
```

---

## Success Metrics Per Version

### 1_MVP_base
- ✅ Bot completes conversation (80%+ completion rate)
- ✅ Correct specialty match (85%+ accuracy)
- ✅ <10 second response time
- ✅ Zero cost operation

### 2_MVP_enhanced
- ✅ Multi-field extraction works (95%+ accuracy)
- ✅ Reduces question count by 30%
- ✅ Better user satisfaction
- ✅ <5 second response time

### 3_appointment_booking
- ✅ 50%+ of recommendations → bookings
- ✅ <1% booking errors
- ✅ SMS delivery 99%+
- ✅ User can complete booking in <2 min

### 4_location_maps
- ✅ Location accuracy <500m
- ✅ Distance calculation accurate
- ✅ 70%+ users prefer nearby doctors
- ✅ Maps load <3 seconds

### 5_payments
- ✅ Payment success rate 95%+
- ✅ Invoice generation 100%
- ✅ Refund processing <24 hours
- ✅ Zero security incidents

---

## Current Status Summary

| Branch | Status | Features | Database | Deployment |
|--------|--------|----------|----------|------------|
| main | 🟢 Stable | Basic conversation | CSV | Production |
| 1_MVP_base | 🟡 Creating | Baseline snapshot | CSV | Staging |
| dev | 🔵 Active | Intelligent extraction | CSV | Dev only |
| 2_MVP_enhanced | ⚪ Planned | Smart conversation | Enhanced CSV | Not yet |
| 3_appointment_booking | ⚪ Planned | Booking system | SQLite | Not yet |
| 4_location_maps | ⚪ Planned | Maps & proximity | PostgreSQL | Not yet |
| 5_payments | ⚪ Planned | Payment gateway | PostgreSQL | Not yet |
| 6_full_platform | ⚪ Planned | Reviews & analytics | PostgreSQL | Not yet |

---

## Next Immediate Actions

1. ✅ Complete intelligent extraction testing on `dev`
2. 🚧 Create `1_MVP_base` branch as stable checkpoint
3. 📋 Plan database schema for `doctors_enhanced.csv`
4. 📋 Update IMPLEMENTATION_SUMMARY.md with branch strategy
5. 📋 Test and validate `2_MVP_enhanced` features
6. 📋 Merge stable `dev` → `main` after validation

**Current Focus:** Creating stable baseline (`1_MVP_base`) before advancing features.
