# Issue Analysis: Tooth Pain → Oncologist Bug

## Problem Identified

**Chat Flow Result:** Tooth pain was incorrectly matched to **Dr. Faroj Ali M (Medical Oncologist)** and other medical oncologists.

## Root Causes

### 1. **Weak Specialty-Symptom Mapping**
- Current CSV only has `Keywords` column with generic terms
- Keywords like "cancer", "tumor" match oncologist
- Missing explicit specialty→symptom mapping
- No validation that keywords actually relate to the doctor's specialty

### 2. **Vague Keyword Matching**
- Example: Oncologist has keyword "pain" (generic)
- Tooth pain matches "pain" → oncologist selected
- No specificity in keyword categories

### 3. **No Symptom Severity Filtering**
- Dental pain is typically non-urgent
- Oncology is for serious systemic diseases
- No filtering based on severity + specialty combination

### 4. **Missing Dental/ENT Specialty**
- Current database lacks dentists or dental specialists
- No ENT doctors for tooth-related issues
- Generic "General Physician" used as fallback

---

## Solution Strategy

### A. Improved Keyword System
```
Create symptom categories:
- PRIMARY_SYMPTOMS: Direct indicators (e.g., "cavity", "tooth_ache" → Dentist)
- SECONDARY_SYMPTOMS: Related signs (e.g., "swollen jaw" + tooth pain → Dentist)
- EXCLUDE_KEYWORDS: What specialty should NOT handle (e.g., Oncologist excludes "tooth_pain")
```

### B. Specialty-Symptom Mapping Table
```yaml
Dentist:
  primary_symptoms: ["tooth_pain", "cavities", "root_canal", "teeth_whitening", "gum_disease"]
  age_groups: ["All"]
  emergency_capable: true
  
Oncologist:
  primary_symptoms: ["cancer", "tumor", "chemotherapy", "metastasis"]
  secondary_symptoms: ["fatigue", "weight_loss"]
  exclude_keywords: ["tooth", "dental", "ear", "nose", "throat"]
  age_groups: ["Adult", "Geriatric"]
  emergency_capable: false
```

### C. Ranking Algorithm
```
Match Score = (Primary Match × 10) + (Secondary Match × 5) - (Exclude Match × 100)
```

---

## Test Case: Tooth Pain

**User Input:** "tooth pain"
**User Answers:**
- Duration: 3 days
- Severity: 7/10
- Associated: swollen gums
- Age: 45
- Location: Perinthalmanna
- Chronic: None
- Medications: None

**Expected Flow:**
1. LLM identifies: specialty = "Dentist", symptoms = ["tooth_pain", "gum_disease"]
2. Doctor match finds: Dr. Priya (Dentist) with "dental pain" keyword
3. NOT matched to: Oncologist (excluded by negative keyword matching)

**Current Bug:** 
- Oncologist matched because "pain" is too generic
- No specialty validation

**Fix:**
- Add `exclude_keywords` field
- Improve LLM prompts to specify "Dentist" not "General Physician"
- Validate specialty before returning

