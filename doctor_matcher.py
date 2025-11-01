"""
Doctor matching logic using CSV database
"""
import pandas as pd
from config import DOCTORS_DB_PATH


class DoctorMatcher:
    def __init__(self):
        try:
            self.doctors_df = pd.read_csv(DOCTORS_DB_PATH)
            # Fill NaN values for all symptom-related columns
            if 'primary_symptoms' in self.doctors_df.columns:
                self.doctors_df['primary_symptoms'] = self.doctors_df['primary_symptoms'].fillna('')
            if 'secondary_symptoms' in self.doctors_df.columns:
                self.doctors_df['secondary_symptoms'] = self.doctors_df['secondary_symptoms'].fillna('')
            if 'exclude_keywords' in self.doctors_df.columns:
                self.doctors_df['exclude_keywords'] = self.doctors_df['exclude_keywords'].fillna('')
            # Backward compatibility with old CSV format
            if 'Keywords' in self.doctors_df.columns:
                self.doctors_df['Keywords'] = self.doctors_df['Keywords'].fillna('')
            print(f"Loaded {len(self.doctors_df)} doctors from database")
        except FileNotFoundError:
            print(f"Error: The doctors database at '{DOCTORS_DB_PATH}' was not found.")
            self.doctors_df = pd.DataFrame()  # Create an empty DataFrame
    
    def find_doctors(self, symptoms, specialty=None, online_only=False, limit=3):
        """
        Find matching doctors based on symptoms and specialty with exclude keywords
        Enhanced algorithm to prevent mismatches (e.g., tooth pain → oncologist)
        """
        matches = []
        
        if self.doctors_df.empty:
            return []
            
        for idx, doctor in self.doctors_df.iterrows():
            score = 0
            
            # STEP 1: Check exclude keywords (NEGATIVE MATCH - prevents wrong matches)
            exclude_keywords = str(doctor.get('exclude_keywords', '')).lower()
            if exclude_keywords and exclude_keywords != 'nan':
                excluded_terms = [term.strip() for term in exclude_keywords.split(',') if term.strip()]
                should_exclude = False
                for symptom in symptoms:
                    symptom_clean = symptom.lower().strip()
                    for excluded_term in excluded_terms:
                        if symptom_clean in excluded_term or excluded_term in symptom_clean:
                            should_exclude = True
                            break
                    if should_exclude:
                        break
                
                if should_exclude:
                    continue  # Skip this doctor entirely
            
            # STEP 2: Check specialty match (PRIMARY MATCH)
            if specialty and specialty.lower() in str(doctor.get('Specialty', '')).lower():
                score += 20
            
            # STEP 3: Check primary symptoms (HIGH WEIGHT)
            primary_symptoms = str(doctor.get('primary_symptoms', '')).lower()
            if primary_symptoms and primary_symptoms != 'nan':
                primary_terms = [term.strip() for term in primary_symptoms.split(',') if term.strip()]
                for symptom in symptoms:
                    symptom_clean = symptom.lower().strip()
                    for primary_term in primary_terms:
                        if symptom_clean in primary_term or primary_term in symptom_clean:
                            score += 10
            
            # STEP 4: Check secondary symptoms (MEDIUM WEIGHT)
            secondary_symptoms = str(doctor.get('secondary_symptoms', '')).lower()
            if secondary_symptoms and secondary_symptoms != 'nan':
                secondary_terms = [term.strip() for term in secondary_symptoms.split(',') if term.strip()]
                for symptom in symptoms:
                    symptom_clean = symptom.lower().strip()
                    for secondary_term in secondary_terms:
                        if symptom_clean in secondary_term or secondary_term in symptom_clean:
                            score += 5
            
            # STEP 5: Fallback to old Keywords column (for legacy data)
            if score == 0:
                keywords = str(doctor.get('Keywords', '')).lower()
                if keywords and keywords != 'nan':
                    keyword_list = [term.strip() for term in keywords.split(',') if term.strip()]
                    for symptom in symptoms:
                        symptom_clean = symptom.lower().strip()
                        for keyword in keyword_list:
                            if symptom_clean in keyword or keyword in symptom_clean:
                                score += 3
            
            if score > 0:
                matches.append({
                    'doctor': doctor,
                    'score': score
                })
        
        # Sort by score and return top matches
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:limit]
    
    def format_doctor_card(self, match):
        """
        Format doctor information for display
        Handles both old CSV format (Doctor_Name) and new format (full_name)
        """
        doctor = match['doctor']
        
        # Handle different column name formats
        doctor_name = doctor.get('full_name', doctor.get('Doctor_Name', 'Unknown'))
        specialty = doctor.get('specialty', doctor.get('Specialty', 'General'))
        clinic_name = doctor.get('clinic_name', doctor.get('Clinic_Name', 'N/A'))
        address = doctor.get('address', doctor.get('Address', 'N/A'))
        phone = doctor.get('phone_number', doctor.get('Phone', ''))
        
        card = f"""
👨‍⚕️ **{doctor_name}**
🏥 {specialty}
📍 {clinic_name}
📌 {address}
"""
        
        # Add phone if available
        if phone:
            card += f"📞 {phone}\n"
        
        # Add primary symptoms (new format) or keywords (old format)
        if 'primary_symptoms' in doctor and pd.notna(doctor['primary_symptoms']):
            symptoms_list = str(doctor['primary_symptoms']).split(',')[:3]
            card += f"🔍 Treats: {', '.join([s.strip().replace('_', ' ').title() for s in symptoms_list])}\n"
        elif 'Keywords' in doctor and pd.notna(doctor['Keywords']):
            keywords_list = str(doctor['Keywords']).split(',')[:3]
            card += f"🔍 Treats: {', '.join(keywords_list)}\n"
        
        return card