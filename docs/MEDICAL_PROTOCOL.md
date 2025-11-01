# Medical History Protocol for Arogyamitra

## Structured Question Flow (Following SOAP Protocol)

### 1. **Chief Complaint** (Already collected from first message)
   - "What is your main complaint today?"
   - Examples: fever, headache, stomach pain

### 2. **History of Present Illness (HPI)**
   
   **Duration:**
   - "How many days have you had this problem?"
   - Captures: onset, duration
   
   **Severity:**
   - "On a scale of 1-10, how severe is it?"
   - Helps prioritize urgency
   
   **Associated Symptoms:**
   - "Do you have any other symptoms?"
   - Examples: nausea, vomiting, dizziness, fatigue
   
### 3. **Patient Demographics**
   
   **Age:**
   - "What is your age?"
   - Critical for diagnosis (pediatric vs adult vs geriatric)
   
   **Location:**
   - "Which area in Kerala are you from?"
   - For doctor proximity matching

### 4. **Past Medical History (PMH)**
   
   **Chronic Conditions:**
   - "Do you have any chronic conditions?"
   - Examples: diabetes, hypertension, asthma
   
   **Current Medications:**
   - "Are you taking any medications currently?"
   - Important for drug interactions and diagnosis

### 5. **Triage & Recommendation**
   - AI analyzes all collected data
   - Follows clinical decision-making
   - Recommends appropriate specialty
   - Matches to doctors in database

---

## Database Improvements Needed

### Current CSV Columns:
- Doctor_Name
- Specialty
- Clinic_Name
- Address
- Pincode
- Keywords

### Recommended Additional Columns:

#### 1. **Availability & Scheduling**
   - `consultation_days` (Mon-Fri, Weekends, etc.)
   - `consultation_hours` (9AM-5PM, etc.)
   - `online_consult` (Yes/No)
   - `appointment_required` (Yes/No/Walk-in)
   - `average_wait_time` (15min, 30min, etc.)

#### 2. **Contact & Booking**
   - `phone_number` (for direct contact)
   - `whatsapp_number`
   - `email`
   - `website_url`
   - `booking_link` (online appointment)

#### 3. **Doctor Details**
   - `qualification` (MBBS, MD, MS, etc.)
   - `experience_years`
   - `sub_specialties` (e.g., "Pediatric Cardiology")
   - `languages_spoken` (Malayalam, English, Hindi)
   - `gender` (for patient preference)

#### 4. **Clinical Capabilities**
   - `procedures_offered` (Minor surgery, ECG, X-ray, etc.)
   - `diagnostic_facilities` (Lab, Imaging, etc.)
   - `emergency_services` (Yes/No)
   - `insurance_accepted` (list of accepted insurance)

#### 5. **Patient Experience**
   - `consultation_fee_range` (₹300-500)
   - `accepts_new_patients` (Yes/No)
   - `accessibility` (Wheelchair, Parking, etc.)
   - `patient_rating` (1-5 stars, if available)

#### 6. **Location & Navigation**
   - `latitude` (for map integration)
   - `longitude`
   - `landmark` (near X hospital, Y junction)
   - `google_maps_link`

#### 7. **Matching & Filtering**
   - `conditions_treated` (expanded keywords by condition)
   - `age_groups_treated` (Pediatric, Adult, Geriatric, All)
   - `urgent_care_available` (Yes/No)

---

## Clinical Decision Support

### Symptom → Specialty Mapping Examples:

**Fever + Cough**
- Primary: General Physician
- If persistent: Pulmonologist

**Chest Pain**
- Emergency flag → Cardiologist + Emergency Medicine
- Mild: General Physician

**Stomach Pain**
- Duration <3 days: General Physician
- Duration >3 days: Gastroenterologist

**Skin Rash**
- Direct to: Dermatologist

**Joint Pain**
- Acute: Orthopedist
- Chronic: Rheumatologist

---

## Benefits of Structured Approach:

✅ **Shorter, clearer questions** - easier for patients
✅ **Complete medical history** - better recommendations
✅ **Clinical validity** - follows medical protocols
✅ **Better matching** - more accurate doctor selection
✅ **Urgency detection** - identifies emergencies faster
✅ **Consistent data** - easier to analyze and improve
