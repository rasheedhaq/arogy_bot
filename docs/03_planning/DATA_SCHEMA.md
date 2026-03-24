# Complete Medical Platform Data Schema

## Phase 1: MVP (Current - Symptoms → Doctor List)
## Phase 2: Enhanced (Add Availability + Booking)
## Phase 3: Full (Add Payments + Reviews)

---

# DOCTORS TABLE - Complete Schema

## Core Information (Required for MVP)

| Field | Type | Format | Example | Purpose |
|-------|------|--------|---------|---------|
| **doctor_id** | String | UUID/auto | `DOC_001` | Unique identifier |
| **full_name** | String | Text | `Dr. Priya Sharma` | Doctor display name |
| **specialty** | String | Enum | `Dentist` `Cardiologist` `Orthopedist` | Primary specialty |
| **sub_specialty** | String | Text | `Pediatric Cardiology` | Specialization area |
| **qualification** | String | Text | `BDS, MDS` | Degrees |
| **experience_years** | Integer | Number | `12` | Years practicing |

---

## Symptom Matching (Critical for Bug Fix)

| Field | Type | Format | Example | Purpose |
|-------|------|--------|---------|---------|
| **primary_symptoms** | Array | CSV/JSON | `"tooth_pain,cavity,gum_disease"` | Direct indicators for this doctor |
| **secondary_symptoms** | Array | CSV/JSON | `"jaw_pain,mouth_sores"` | Related symptoms (lower weight) |
| **exclude_keywords** | Array | CSV/JSON | `"cancer,tumor,skin"` | What this doctor should NOT match |
| **age_groups_treated** | Array | Enum | `"Pediatric,Adult,Geriatric"` | Age specialization |
| **emergency_capable** | Boolean | true/false | `true` | Can handle urgent cases |

---

## Location & Availability (Phase 2)

| Field | Type | Format | Example | Purpose |
|-------|------|--------|---------|---------|
| **clinic_name** | String | Text | `Smile Dental Clinic` | Clinic/hospital name |
| **address** | String | Text | `123 Main St` | Full street address |
| **pincode** | String | 6-digit | `670331` | Postal code for location filtering |
| **city** | String | Enum | `Malappuram` | City name |
| **latitude** | Float | Decimal | `11.0089` | GPS coordinate |
| **longitude** | Float | Decimal | `76.2411` | GPS coordinate |
| **google_maps_link** | String | URL | `https://goo.gl/maps/...` | Direct map link |

---

## Contact Information (Phase 2)

| Field | Type | Format | Example | Purpose |
|-------|------|--------|---------|---------|
| **phone_number** | String | 10-digit | `9876543210` | Primary contact |
| **whatsapp_number** | String | 10-digit | `9876543210` | WhatsApp contact |
| **email** | String | Email | `doctor@clinic.com` | Email address |
| **website_url** | String | URL | `https://clinic.com` | Clinic website |

---

## Availability & Booking (Phase 2)

| Field | Type | Format | Example | Purpose |
|-------|------|--------|---------|---------|
| **consultation_days** | Array | Enum | `"Mon,Tue,Wed,Thu,Fri,Sat"` | Available days |
| **consultation_hours_start** | String | HH:MM | `09:00` | Clinic opening time |
| **consultation_hours_end** | String | HH:MM | `18:00` | Clinic closing time |
| **online_consult_available** | Boolean | true/false | `true` | Video consultation option |
| **appointment_required** | Boolean | true/false | `true` | Must book in advance |
| **average_wait_time_mins** | Integer | Minutes | `20` | Expected wait time |
| **slots_available_today** | Integer | Count | `5` | Real-time (from booking system) |

---

## Consultation Details (Phase 2-3)

| Field | Type | Format | Example | Purpose |
|-------|------|--------|---------|---------|
| **consultation_fee** | Integer | Amount in ₹ | `500` | Cost per consultation |
| **insurance_accepted** | String | Enum list | `"Aetna,Bajaj,Star,ICICI"` | Accepted insurances |
| **online_fee** | Integer | Amount in ₹ | `400` | Video consultation cost |
| **home_visit_available** | Boolean | true/false | `false` | Home consultation |
| **home_visit_fee** | Integer | Amount in ₹ | `1000` | House visit cost |

---

## Clinic Facilities (Phase 2-3)

| Field | Type | Format | Example | Purpose |
|-------|------|--------|---------|---------|
| **diagnostic_services** | Array | Text | `"X-ray,ECG,Lab"` | Available tests |
| **procedures_offered** | Array | Text | `"Root canal,Tooth extraction"` | Treatments |
| **emergency_services** | Boolean | true/false | `true` | 24/7 availability |
| **parking_available** | Boolean | true/false | `true` | Parking facility |
| **wheelchair_accessible** | Boolean | true/false | `true` | Accessibility |
| **languages_spoken** | Array | Enum | `"Malayalam,English,Hindi"` | Doctor languages |

---

## Patient Experience (Phase 3)

| Field | Type | Format | Example | Purpose |
|-------|------|--------|---------|---------|
| **average_rating** | Float | 1-5 stars | `4.5` | Patient reviews |
| **total_reviews** | Integer | Count | `127` | Number of reviews |
| **accepts_new_patients** | Boolean | true/false | `true` | Accepting new patients |
| **cancellation_policy** | String | Text | `"Free upto 24hrs"` | Booking policy |

---

## Payment Integration (Phase 3)

| Field | Type | Format | Example | Purpose |
|-------|------|--------|---------|---------|
| **payment_gateway_id** | String | ID | `GATEWAY_001` | Razorpay/Paypal ID |
| **refund_policy** | String | Text | `"100% within 24hrs"` | Refund terms |
| **installment_available** | Boolean | true/false | `false` | Installment option |

---

# Data Format Examples

## CSV Format (Easy for data entry)

```csv
doctor_id,full_name,specialty,sub_specialty,qualification,experience_years,primary_symptoms,secondary_symptoms,exclude_keywords,age_groups_treated,emergency_capable,clinic_name,address,pincode,city,latitude,longitude,phone_number,email,consultation_days,consultation_hours_start,consultation_hours_end,online_consult_available,consultation_fee,insurance_accepted

DOC_D001,Dr. Priya Sharma,Dentist,Pediatric Dentistry,BDS MDS,12,"tooth_pain,cavity,gum_disease,teeth_whitening","jaw_pain,mouth_sores,tooth_sensitivity","cancer,tumor,skin,heart",Pediatric Adult,true,Smile Dental Clinic,123 Main Street,670331,Malappuram,11.0089,76.2411,9876543210,priya@smiledental.com,"Mon,Tue,Wed,Thu,Fri,Sat",09:00,18:00,true,500,"Aetna,Bajaj"

DOC_C001,Dr. Rajesh Kumar,Cardiologist,Interventional Cardiology,MD DM,18,"chest_pain,heart_palpitations,shortness_breath","dizziness,fatigue,high_bp","tooth,skin,dental,orthopedic",Adult Geriatric,true,Heart Care Hospital,456 Hospital Road,670332,Malappuram,11.0095,76.2420,9876543211,rajesh@heartcare.com,"Mon,Tue,Wed,Thu,Fri",08:00,17:00,true,1000,"ICICI,Star"

DOC_O001,Dr. Arjun Singh,Orthopedist,Sports Medicine,MBBS MS,15,"joint_pain,fracture,sports_injury,back_pain","muscle_strain,swelling,weakness","cancer,tooth,skin,heart",Adult Geriatric,false,Ortho Clinic Plus,789 Sports Lane,670333,Malappuram,11.0080,76.2400,9876543212,arjun@orthoclinic.com,"Mon,Wed,Fri,Sat",10:00,19:00,false,400,"Star,National"
```

---

# Specialty-to-Symptoms Mapping Table

## Reference for Accurate Matching

| Specialty | Primary Symptoms | Exclude | Common Errors |
|-----------|------------------|---------|----------------|
| **Dentist** | tooth_pain, cavity, gum_disease, teeth_whitening, root_canal, tooth_extraction, braces | cancer, tumor, heart, lung | Tooth pain → General Physician ❌ |
| **Cardiologist** | chest_pain, heart_palpitation, shortness_breath, high_bp, arrhythmia | tooth, skin, orthopedic, cancer | Chest tightness → anxiety ❌ |
| **Orthopedist** | joint_pain, fracture, back_pain, sports_injury, ACL_tear, arthritis | tooth, heart, skin, cancer | Back pain → General Physician ❌ |
| **Dermatologist** | skin_rash, acne, eczema, psoriasis, hair_loss, moles | tooth, heart, orthopedic, cancer | Skin rash → General Physician ❌ |
| **Pulmonologist** | cough_persistent, shortness_breath, asthma, tuberculosis, chest_pain_lung | tooth, heart_arrhythmia, orthopedic | Cough → General Physician ❌ |
| **General Physician** | fever, cold, cough_mild, diarrhea, headache, body_ache | tooth, heart_serious, cancer, trauma | Fever → specific specialist ❌ |
| **Gastroenterologist** | stomach_pain, acidity, ulcer, constipation, diarrhea, vomiting | tooth, heart, orthopedic | Stomach pain → General Physician ❌ |
| **ENT** | ear_pain, throat_pain, sinusitis, hearing_loss, tinnitus | tooth, heart, orthopedic, cancer | Throat pain → General Physician ❌ |

---

# How to Fix the Oncologist Bug

## Before (Current CSV)
```csv
doctor_id,full_name,specialty,keywords
DOC_O001,Dr. Faroj Ali M,Medical Oncologist,"cancer,tumor,pain,fatigue"
```
❌ **Problem:** "pain" matches tooth_pain

## After (New Schema)
```csv
doctor_id,full_name,specialty,primary_symptoms,secondary_symptoms,exclude_keywords
DOC_O001,Dr. Faroj Ali M,Medical Oncologist,"cancer,tumor,chemotherapy,metastasis","fatigue,weight_loss","tooth,dental,ear,nose,throat,orthopedic"
```
✅ **Solution:** "cancer" specific, "tooth" explicitly excluded

---

# Implementation Priority

### Must Have (MVP)
- ✅ specialty
- ✅ primary_symptoms
- ✅ exclude_keywords (FIX FOR ONCOLOGIST BUG)
- ✅ clinic_name, address, pincode
- ✅ phone_number, email

### Should Have (Phase 2)
- ⏳ consultation_days, consultation_hours
- ⏳ consultation_fee
- ⏳ latitude, longitude
- ⏳ online_consult_available

### Nice to Have (Phase 3)
- ⏳ average_rating
- ⏳ insurance_accepted
- ⏳ payment_gateway_id

