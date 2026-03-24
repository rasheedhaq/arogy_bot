# Quick Start Data Collection Template

**For: Data Entry Team**

---

## How to Fill This Form

This CSV template is designed for easy data entry. Just fill in the columns left-to-right.

### What to Collect from Each Doctor

1. **Basic Info** - Ask doctor directly
2. **Symptoms** - Based on their specialty (see reference below)
3. **Contact** - From clinic
4. **Schedule** - When they work
5. **Fees** - What they charge

---

## Column-by-Column Guide

### MANDATORY (Must Fill)

| Column | What to Enter | Example | How |
|--------|---------------|---------|-----|
| **doctor_id** | Doctor code | DOC_D002 | Doc_ + specialty code + number |
| **full_name** | Doctor's full name | Dr. Akshay Mehta | From clinic |
| **specialty** | Type of doctor | Dentist / Cardiologist / etc | Ask doctor |
| **qualification** | Degrees | BDS MDS or MD DM | Certificate |
| **experience_years** | Years practicing | 10 | Ask doctor |
| **clinic_name** | Hospital/clinic name | ABC Dental Center | Sign board |
| **address** | Full address | 123 Main St, Perinthalmanna | From sign board |
| **pincode** | 6-digit postal code | 670331 | Postal code |
| **phone_number** | 10-digit number | 9876543210 | Clinic number |
| **email** | Email address | doctor@clinic.com | Business card |

### PRIMARY SYMPTOMS (Most Important - Prevents Tooth→Oncologist Bug)

| Column | What to Enter | Example | Rules |
|--------|---------------|---------|-------|
| **primary_symptoms** | Main symptoms this doctor treats | "tooth_pain,cavity,gum_disease" | Use list below |
| **exclude_keywords** | What to AVOID | "cancer,tumor,heart" | Opposite specialties |

### SCHEDULE & FEES

| Column | What to Enter | Example | How |
|--------|---------------|---------|-----|
| **consultation_days** | Working days | "Mon,Tue,Wed,Thu,Fri,Sat" | Ask clinic |
| **consultation_hours_start** | Opening time | 09:00 | Ask clinic |
| **consultation_hours_end** | Closing time | 18:00 | Ask clinic |
| **consultation_fee** | Fee per visit | 500 | Ask doctor |
| **online_consult_available** | Video consultation? | true/false | Ask clinic |

### OPTIONAL (Nice to Have)

| Column | What to Enter | Example |
|--------|---------------|---------|
| **sub_specialty** | Focused area | Pediatric Dentistry |
| **latitude** | GPS coordinate | 11.0089 |
| **longitude** | GPS coordinate | 76.2411 |
| **diagnostic_services** | Tests available | "X-ray,CBCT" |
| **procedures_offered** | Treatments | "Root canal,Extraction" |

---

## Specialty → Primary Symptoms Mapping

**Copy the right symptoms for the doctor's specialty:**

### DENTIST
```
Primary: tooth_pain,cavity,gum_disease,teeth_whitening,root_canal,tooth_extraction,braces,tooth_sensitivity,oral_ulcer
Secondary: jaw_pain,mouth_sores,swollen_gums,teeth_grinding
Exclude: cancer,tumor,skin,heart,lung,orthopedic
```

### CARDIOLOGIST
```
Primary: chest_pain,heart_palpitation,shortness_breath,high_bp,arrhythmia,heart_murmur,coronary_artery_disease
Secondary: dizziness,fatigue,sweating,leg_swelling,irregular_heartbeat
Exclude: tooth,skin,dental,orthopedic,ear,nose,throat
```

### ORTHOPEDIST
```
Primary: joint_pain,fracture,back_pain,sports_injury,knee_pain,shoulder_pain,arthritis,ACL_tear,ligament_injury
Secondary: muscle_strain,swelling,weakness,stiffness,bruising
Exclude: cancer,tooth,skin,heart,lung,dental
```

### GASTROENTEROLOGIST
```
Primary: stomach_pain,acidity,ulcer,constipation,diarrhea,vomiting,bloating,gas,heartburn,food_poisoning
Secondary: nausea,loss_appetite,weight_loss,abdominal_discomfort
Exclude: tooth,heart,orthopedic,skin,cancer
```

### ENT (Ear, Nose, Throat)
```
Primary: ear_pain,throat_pain,sinusitis,hearing_loss,tinnitus,deviated_septum,allergic_rhinitis,voice_loss,tonsillitis
Secondary: ear_discharge,nasal_congestion,snoring,hoarseness
Exclude: tooth,heart,orthopedic,skin,cancer
```

### DERMATOLOGIST
```
Primary: skin_rash,acne,eczema,psoriasis,hair_loss,moles,warts,fungal_infection,lichen_planus,vitiligo
Secondary: itching,redness,scaling,discoloration
Exclude: tooth,heart,orthopedic,cancer,lung
```

### PULMONOLOGIST
```
Primary: cough_persistent,shortness_breath,asthma,tuberculosis,chest_pain_lung,wheezing,bronchitis,emphysema
Secondary: fever,fatigue,body_ache,night_sweats
Exclude: tooth,heart_simple,orthopedic,skin,cancer_non_lung
```

### GENERAL PHYSICIAN
```
Primary: fever,cold,cough_mild,diarrhea,headache,body_ache,infection,common_illness,blood_pressure_check,wellness_checkup
Secondary: fatigue,loss_appetite,mild_pain
Exclude: cancer,serious_heart,orthopedic_trauma,dental_extraction
```

### NEUROLOGIST
```
Primary: headache_severe,migraine,dizziness,vertigo,seizure,memory_loss,tremor,neuropathy,stroke_symptoms
Secondary: weakness,numbness,balance_problem,vision_issue
Exclude: tooth,heart_simple,orthopedic,skin,cancer_non_neuro
```

### PSYCHIATRIST
```
Primary: depression,anxiety,stress,insomnia,panic_disorder,bipolar_disorder,schizophrenia,ocd,ptsd
Secondary: mood_change,behavior_change,concentration_issue
Exclude: tooth,heart_simple,orthopedic,skin,cancer
```

### ENDOCRINOLOGIST
```
Primary: diabetes,thyroid_disorder,thyroiditis,goiter,hypothyroidism,hyperthyroidism,hormone_imbalance,obesity_related
Secondary: fatigue,weight_change,temperature_sensitivity,hair_thinning
Exclude: tooth,heart_arrhythmia,orthopedic,skin,cancer_non_endocrine
```

### NEPHROLOGIST
```
Primary: kidney_pain,kidney_disease,dialysis_related,high_creatinine,proteinuria,kidney_stones,urinary_issues
Secondary: swelling,high_bp,fatigue,nausea
Exclude: tooth,heart_simple,orthopedic,skin,cancer_non_kidney
```

---

## Filled Example

```csv
doctor_id,full_name,specialty,qualification,experience_years,primary_symptoms,exclude_keywords,clinic_name,address,pincode,phone_number,email,consultation_days,consultation_hours_start,consultation_hours_end,consultation_fee,online_consult_available

DOC_D005,Dr. Anil Nambiar,Dentist,BDS,8,"tooth_pain,cavity,gum_disease,root_canal,teeth_whitening","cancer,tumor,heart,lung",Bright Smile Dental,45 Medical Complex Road Perinthalmanna,670331,9876543225,anil@brightsmile.com,"Mon,Tue,Wed,Thu,Fri,Sat",09:00,17:30,400,true
```

---

## Quick Checklist

Before submitting doctor data:

- [ ] Doctor ID filled? (DOC_XXX format)
- [ ] Name correct?
- [ ] Specialty matches one from list?
- [ ] Phone number is 10 digits?
- [ ] Email looks valid?
- [ ] Primary symptoms copied from reference?
- [ ] Exclude keywords filled (prevents wrong matches)?
- [ ] Consultation fee filled?
- [ ] Hours look reasonable? (not 00:00-00:00)
- [ ] At least one day of consultation marked?

---

## How to Avoid the Oncologist Bug

❌ **WRONG:**
```csv
specialty,keywords
Medical Oncologist,"cancer,pain,fatigue"
```
→ Will match tooth_pain to oncologist (BAD!)

✅ **RIGHT:**
```csv
specialty,primary_symptoms,exclude_keywords
Medical Oncologist,"cancer,tumor,chemotherapy,metastasis","tooth,dental,ear,nose,throat,orthopedic"
```
→ Will NOT match tooth_pain to oncologist (GOOD!)

**KEY:** Always fill `exclude_keywords` to prevent mismatches!

---

## Questions to Ask Doctor

1. **Name & Qualification:** "What's your full name and degrees?"
2. **Experience:** "How many years have you been practicing?"
3. **Specialties:** "What do you primarily treat?"
4. **Schedule:** "What are your clinic hours and working days?"
5. **Fees:** "What's your consultation fee?"
6. **Services:** "Do you offer online consultations?"
7. **Facilities:** "What diagnostic services do you have?"

---

## Submission Format

Save as: `doctors_[CITY]_[DATE].csv`

Example: `doctors_malappuram_2025_01_15.csv`

Send to: [Your Email]

---

## Support

For questions about:
- **Specialty codes:** See mapping above
- **CSV format:** Check example in FULL_PLATFORM_ROADMAP.md
- **Phone validation:** Must be 10 digits, no spaces/dashes
- **Symptoms list:** Use exact terms from reference tables

