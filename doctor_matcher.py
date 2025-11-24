"""
Doctor matching logic using CSV database
"""
import pandas as pd
from typing import List, Dict, Optional, Any
from config import DOCTORS_DB_PATH
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DoctorMatcher:
    def __init__(self, db_path: str = DOCTORS_DB_PATH):
        """
        Initialize DoctorMatcher with the database path.
        """
        self.doctors_df = self._load_database(db_path)
    
    def _load_database(self, db_path: str) -> pd.DataFrame:
        """
        Load and preprocess the doctors database.
        """
        try:
            df = pd.read_csv(db_path)
            # Fill NaN values for all symptom-related columns
            text_columns = ['primary_symptoms', 'secondary_symptoms', 'exclude_keywords', 'Keywords', 'specialty', 'Specialty']
            for col in text_columns:
                if col in df.columns:
                    df[col] = df[col].fillna('')
            
            logger.info(f"Loaded {len(df)} doctors from database")
            return df
        except FileNotFoundError:
            logger.error(f"Error: The doctors database at '{db_path}' was not found.")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Failed to load doctors database: {e}")
            return pd.DataFrame()

    def find_doctors(self, symptoms: List[str], specialty: Optional[str] = None, online_only: bool = False, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Find matching doctors based on symptoms and specialty with exclude keywords.
        """
        if self.doctors_df.empty:
            return []
            
        matches = []
        
        for _, doctor in self.doctors_df.iterrows():
            score = self._calculate_score(doctor, symptoms, specialty)
            
            if score > 0:
                matches.append({
                    'doctor': doctor.to_dict(),
                    'score': score
                })
        
        # Sort by score and return top matches
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:limit]

    def _calculate_score(self, doctor: pd.Series, symptoms: List[str], specialty: Optional[str]) -> int:
        """
        Calculate match score for a single doctor.
        Returns 0 if excluded or no match.
        """
        # STEP 1: Check exclude keywords (NEGATIVE MATCH)
        if self._is_excluded(doctor, symptoms):
            return 0
            
        score = 0
        
        # STEP 2: Check specialty match (PRIMARY MATCH)
        if specialty and self._matches_specialty(doctor, specialty):
            score += 20
            
        # STEP 3: Check primary symptoms (HIGH WEIGHT)
        score += self._match_symptoms(doctor, symptoms, 'primary_symptoms', 10)
        
        # STEP 4: Check secondary symptoms (MEDIUM WEIGHT)
        score += self._match_symptoms(doctor, symptoms, 'secondary_symptoms', 5)
        
        # STEP 5: Fallback to old Keywords column
        if score == 0:
            score += self._match_symptoms(doctor, symptoms, 'Keywords', 3)
            
        return score

    def _is_excluded(self, doctor: pd.Series, symptoms: List[str]) -> bool:
        """Check if doctor should be excluded based on keywords."""
        exclude_keywords = str(doctor.get('exclude_keywords', '')).lower()
        if not exclude_keywords:
            return False
            
        excluded_terms = [term.strip() for term in exclude_keywords.split(',') if term.strip()]
        for symptom in symptoms:
            symptom_clean = symptom.lower().strip()
            for excluded_term in excluded_terms:
                if symptom_clean in excluded_term or excluded_term in symptom_clean:
                    return True
        return False

    def _matches_specialty(self, doctor: pd.Series, target_specialty: str) -> bool:
        """Check if doctor matches the target specialty."""
        doctor_specialty = str(doctor.get('specialty', doctor.get('Specialty', ''))).lower()
        specialty_lower = target_specialty.lower()
        
        return (specialty_lower in doctor_specialty or 
                doctor_specialty in specialty_lower or
                specialty_lower.replace('ry', '') in doctor_specialty or
                specialty_lower.replace('logy', '') in doctor_specialty)

    def _match_symptoms(self, doctor: pd.Series, symptoms: List[str], column: str, weight: int) -> int:
        """Calculate score contribution from a symptom column."""
        column_content = str(doctor.get(column, '')).lower()
        if not column_content:
            return 0
            
        score = 0
        terms = [term.strip() for term in column_content.split(',') if term.strip()]
        
        for symptom in symptoms:
            symptom_clean = symptom.lower().strip()
            for term in terms:
                if symptom_clean in term or term in symptom_clean:
                    score += weight
                    # Count each user symptom only once per column type.
                    break 
        return score

    def format_doctor_card(self, match: Dict[str, Any]) -> str:
        """
        Format doctor information for display.
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
        if phone:
            card += f"📞 {phone}\n"
        
        if doctor.get('primary_symptoms'):
            symptoms_list = str(doctor['primary_symptoms']).split(',')[:3]
            card += f"🔍 Treats: {', '.join([s.strip().replace('_', ' ').title() for s in symptoms_list])}\n"
        elif doctor.get('Keywords'):
            keywords_list = str(doctor['Keywords']).split(',')[:3]
            card += f"🔍 Treats: {', '.join(keywords_list)}\n"
        
        return card