# Visual Platform Architecture & Data Flow

## End-to-End System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AROGYAMITRA MEDICAL BOT                              │
│                     Symptoms → Doctors → Booking → Payment                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│                              PHASE 1: MVP (NOW)                               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  USER              BOT              LLM            DATABASE      RESPONSE     │
│  ────              ───              ───            ────────      ────────     │
│                                                                               │
│  "tooth pain"  ──→  Question 1      Groq LLM       CSV File      "8 Questions"│
│                 ──→  Question 2     (llama-3.3)    (19 doctors)              │
│  [Answers ...]  ──→  ...                                                     │
│                 ──→  Question 8    Analyze       Match Score:    "Dr. Priya  │
│                                    Specialty    - Dentist: 95     (Dentist)  │
│                      Extract JSON   & Symptoms  - GP: 40                     │
│                      {                                                        │
│                        "specialty": "Dentist",  Exclude Check:              │
│                        "symptoms": ["tooth_pain"]  "tooth" NOT in           │
│                      }                         "Medical Oncologist"         │
│                                                exclude_keywords ✓            │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 2: AVAILABILITY (WEEK 2-3)                      │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Doctor Selected  ──→  Check Availability                                    │
│                        (From CSV: consultation_days, hours)                   │
│                                                                               │
│                        ┌─────────────────────────────┐                       │
│                        │  CALENDAR INTEGRATION        │                       │
│                        ├─────────────────────────────┤                       │
│                        │ Today (Mon): 3 slots @ 2PM  │                       │
│                        │ Tomorrow: 5 slots @ 10AM    │                       │
│                        │ Online: Available 2-6PM     │                       │
│                        └─────────────────────────────┘                       │
│                                │                                              │
│                                ↓                                              │
│                        SELECT TIME SLOT                                       │
│                        │ Example: Tomorrow 10:15 AM │                        │
│                                                                               │
│  Data Source: CSV (consultation_days, hours) + Real-time slot API           │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│                      PHASE 3: LOCATION FILTERING (WEEK 3-4)                   │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Doctor List + Location Filtering                                            │
│                                                                               │
│  User Location: 670331 (Perinthalmanna)                                      │
│                          │                                                    │
│                          ↓                                                    │
│              ┌─────────────────────────┐                                     │
│              │  GOOGLE MAPS INTEGRATION │                                     │
│              ├─────────────────────────┤                                     │
│              │ Dr. Priya Dental        │                                     │
│              │ ✅ 2.3 km away          │                                     │
│              │ 📍 123 Main St          │                                     │
│              │    Perinthalmanna       │                                     │
│              │                         │                                     │
│              │ Dr. Arjun Orthopedist   │                                     │
│              │ ✅ 5.1 km away          │                                     │
│              │ 📍 789 Sports Lane      │                                     │
│              │    Malappuram          │                                     │
│              └─────────────────────────┘                                     │
│                          │                                                    │
│                          ↓                                                    │
│              [Sort by Distance] [Show on Map]                                │
│                                                                               │
│  Data: CSV (latitude, longitude, address) + Google Maps API                  │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 4: BOOKING (WEEK 4-6)                           │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Select Doctor & Time  ──→  Enter Patient Details                            │
│                              - Name                                           │
│                              - Age, Gender                                    │
│                              - Phone, Email                                   │
│                              - Home Address                                   │
│                                      │                                        │
│                                      ↓                                        │
│                        ┌──────────────────────────┐                          │
│                        │ CONFIRM APPOINTMENT      │                          │
│                        ├──────────────────────────┤                          │
│                        │ Dr. Priya               │                          │
│                        │ Tomorrow, 10:15 AM      │                          │
│                        │ Smile Dental Clinic     │                          │
│                        │ 📍 123 Main St          │                          │
│                        │                          │                          │
│                        │ [CONFIRM] [CANCEL]      │                          │
│                        └──────────────────────────┘                          │
│                                      │                                        │
│                                      ↓                                        │
│                        ✅ BOOKING CONFIRMED                                  │
│                        📧 Email sent                                         │
│                        📱 SMS sent: "Appointment confirmed at Smile Dental"  │
│                                                                               │
│  New Tables: USERS, BOOKINGS                                                │
│  Notifications: SMS (Twillio/AWS SNS), Email                                │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│                       PHASE 5: PAYMENT (WEEK 6-8)                             │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Appointment Confirmed  ──→  [Optional] PAY NOW                              │
│                                          │                                    │
│                                          ↓                                    │
│                              ┌──────────────────────┐                       │
│                              │ RAZORPAY PAYMENT     │                       │
│                              ├──────────────────────┤                       │
│                              │ Consultation Fee: ₹500                       │
│                              │                      │                       │
│                              │ Choose Payment:      │                       │
│                              │ ☐ UPI               │                       │
│                              │ ☐ Card              │                       │
│                              │ ☐ Net Banking       │                       │
│                              │                      │                       │
│                              │ [PAY SECURELY]      │                       │
│                              └──────────────────────┘                       │
│                                          │                                    │
│                                          ↓                                    │
│                  ✅ PAYMENT SUCCESSFUL (Razorpay)                            │
│                  📄 Invoice generated                                        │
│                  💰 Settlement in 2 days                                     │
│                  📋 Status: Paid                                             │
│                                                                               │
│  Payment Gateway: Razorpay                                                   │
│  Commission: 2% + ₹3 per transaction                                         │
│  New Table: PAYMENTS                                                         │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 6: REVIEWS & FOLLOW-UP (WEEK 8-10)                   │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  After Appointment  ──→  Rate & Review                                       │
│                                          │                                    │
│                                          ↓                                    │
│                              ┌──────────────────────┐                       │
│                              │ HOW WAS YOUR VISIT? │                       │
│                              ├──────────────────────┤                       │
│                              │ ⭐⭐⭐⭐⭐ 5 Stars │                       │
│                              │                      │                       │
│                              │ "Dr. Priya was      │                       │
│                              │ very helpful and    │                       │
│                              │ professional"       │                       │
│                              │                      │                       │
│                              │ [SUBMIT REVIEW]     │                       │
│                              └──────────────────────┘                       │
│                                          │                                    │
│                                          ↓                                    │
│          ✅ REVIEW PUBLISHED ON DOCTOR PROFILE                               │
│                                                                               │
│                              FOLLOW-UP OPTIONS                               │
│                              ├─ Schedule next appointment                    │
│                              ├─ Ask a question                               │
│                              └─ View medical records                         │
│                                                                               │
│  New Table: REVIEWS, FOLLOW_UPS                                              │
│  Features: Analytics, Doctor ratings, Recommendations                        │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## Database Schema Evolution

### Phase 1 (MVP - Current)
```csv
doctor_id | full_name | specialty | primary_symptoms | exclude_keywords | 
clinic_name | address | pincode | phone | email
```
**Size:** ~20 columns (doctor table only)

### Phase 2-3
```csv
(Phase 1) + consultation_days | hours_start | hours_end | online_consult | 
appointment_required | latitude | longitude | consultation_fee
```
**Size:** ~30 columns (doctor table only)

### Phase 4
```
USERS table:
user_id | phone | name | age | gender | email | address | created_at

BOOKINGS table:
booking_id | user_id | doctor_id | appointment_date | appointment_time | 
consultation_type | status | created_at

DOCTORS table: (Phase 1-3 fields)
```
**Size:** 3 tables, ~50 total columns

### Phase 5
```
(Phase 4) +

PAYMENTS table:
payment_id | booking_id | amount | payment_method | payment_status | 
transaction_id | razorpay_order_id | created_at
```
**Size:** 4 tables, ~60 total columns

### Phase 6
```
(Phase 5) +

REVIEWS table:
review_id | booking_id | doctor_id | user_id | rating | comment | created_at

FOLLOW_UPS table:
followup_id | booking_id | scheduled_date | reminder_sent
```
**Size:** 6 tables, ~70 total columns

---

## Cost per Phase

```
PHASE 1 (MVP)          PHASE 2              PHASE 3              PHASE 4
┌──────────┐          ┌──────────┐        ┌──────────┐         ┌──────────┐
│ API:     │          │ API:     │        │ API:     │         │ API:     │
│ ₹0       │          │ ₹2000    │        │ ₹2000    │         │ ₹2000    │
│          │          │ (Booking)│        │ (Booking)│         │ (Booking)│
│ SMS: ₹0  │          │          │        │          │         │ SMS:₹500 │
│          │          │ SMS:₹500 │        │ SMS:₹500 │         │          │
│ Total:   │          │          │        │          │         │ Total:   │
│ ₹0/month │          │ Total:   │        │ Total:   │         │ ₹2500/mo │
│          │          │ ₹2500/mo │        │ ₹2500/mo │         │          │
└──────────┘          └──────────┘        └──────────┘         └──────────┘
     ↓                     ↓                    ↓                    ↓
PHASE 5                PHASE 6            SCALING UP
┌──────────┐          ┌──────────┐        ┌──────────┐
│ API:     │          │ API:     │        │ 100K user/month:
│ ₹2000    │          │ ₹2000    │        │ Revenue: ₹500K
│          │          │          │        │ Commission: ₹10K
│ SMS:₹500 │          │ SMS:₹500 │        │ Operating Cost: ₹5K
│          │          │          │        │ Profit: ₹5K/month
│ Payment: │          │ Payment: │        │
│ 2%+₹3    │          │ 2%+₹3    │        │
│          │          │          │        │
│ Total:   │          │ Total:   │        │ Break-even: ~50 bookings/month
│ ₹2500    │          │ ₹2500    │        │ (at ₹500 consultation)
│ +2%      │          │ +2%      │        │
│ per txn  │          │ per txn  │        │ Scales linearly after
└──────────┘          └──────────┘        └──────────┘
```

---

## Data Collection Workflow

```
WEEK 1: Data Preparation
┌────────────────────────────────┐
│ 1. Share DATA_COLLECTION_      │
│    TEMPLATE.md with team       │
│ 2. Explain specialty-symptom   │
│    mapping (prevent bugs)      │
│ 3. Show example: Dentist entry │
│    with exclude_keywords       │
└────────────────────────────────┘
        ↓
        
WEEK 1-2: Data Collection
┌────────────────────────────────┐
│ 1. Data entry person reaches   │
│    out to doctors              │
│ 2. Fills DATA_COLLECTION_      │
│    TEMPLATE.md for each doctor │
│ 3. Saves as:                   │
│    doctors_malappuram_2025_    │
│    01_15.csv                   │
└────────────────────────────────┘
        ↓
        
WEEK 2: Data Validation
┌────────────────────────────────┐
│ 1. Check all mandatory fields  │
│ 2. Verify exclude_keywords     │
│    (prevents tooth→oncologist) │
│ 3. Validate phone numbers      │
│ 4. Test in bot                 │
└────────────────────────────────┘
        ↓
        
WEEK 2-3: Integration
┌────────────────────────────────┐
│ 1. Replace doctors_clean.csv   │
│    with new data               │
│ 2. Restart bot                 │
│ 3. Test tooth pain case        │
│ 4. Deploy to production        │
└────────────────────────────────┘
```

---

## Matching Algorithm Flowchart

```
USER INPUT: "tooth pain"
         ↓
LLM ANALYSIS → specialty: "Dentist", symptoms: ["tooth_pain"]
         ↓
FOR EACH DOCTOR IN DATABASE:
         ↓
[1] CHECK EXCLUDE_KEYWORDS
         ├─ Dentist.exclude_keywords = "cancer,tumor,heart,lung"
         │  ✓ "tooth_pain" NOT in exclude → PASS
         │
         ├─ Medical Oncologist.exclude_keywords = "tooth,dental,ear,nose,throat"
         │  ✗ "tooth_pain" matches "tooth" → SKIP (Score = -∞)
         │
         └─ General Physician.exclude_keywords = "cancer,serious_heart,trauma"
            ✓ "tooth_pain" NOT in exclude → PASS
         ↓
[2] CHECK SPECIALTY MATCH (Weight: 20)
         ├─ Dentist: "Dentist" == "Dentist" → Score += 20
         ├─ Medical Oncologist: SKIPPED (excluded)
         └─ General Physician: "Dentist" != "General Physician" → No match
         ↓
[3] CHECK PRIMARY_SYMPTOMS (Weight: 10)
         ├─ Dentist.primary = "tooth_pain,cavity,gum_disease,root_canal,..."
         │  "tooth_pain" found → Score += 10 (Total: 30)
         │
         └─ General Physician.primary = "fever,cold,cough,diarrhea,..."
            "tooth_pain" NOT found → No match
         ↓
[4] CHECK SECONDARY_SYMPTOMS (Weight: 5)
         ├─ Dentist.secondary = "jaw_pain,mouth_sores,..."
         │  "tooth_pain" NOT found (already in primary) → No additional match
         │
         └─ General Physician.secondary = "fatigue,loss_appetite,..."
            "tooth_pain" NOT found → No match
         ↓
FINAL SCORES:
┌────────────────────────────────┐
│ 1. Dentist: 30                 │
│ 2. General Physician: 0        │
│ 3. Medical Oncologist: SKIPPED │
└────────────────────────────────┘
         ↓
RESULT: Return top 1-2 matches
         ↓
✅ USER GETS: Dr. Priya (Dentist) 30 points
             (NOT Medical Oncologist)
```

---

## Success Checklist

- [ ] Bot runs without errors
- [ ] 8 questions asked in order
- [ ] Tooth pain matches to Dentist (not Oncologist)
- [ ] 2 doctors returned
- [ ] Response time < 10 seconds
- [ ] Telegram message delivered
- [ ] Confirmation SMS received
- [ ] Doctor details formatted correctly
- [ ] No loops or repeated questions
- [ ] All team understands roadmap

