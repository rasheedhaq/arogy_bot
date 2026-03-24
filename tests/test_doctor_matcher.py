import pytest
from app.doctor_matcher import DoctorMatcher
import pandas as pd
import os

class TestDoctorMatcher:
    def test_initialization_no_file(self):
        # Should handle missing file gracefully
        matcher = DoctorMatcher(db_path="data/does_not_exist.csv")
        assert matcher.doctors_df.empty

    def test_find_doctors_basic(self, mock_doctors_csv, monkeypatch):
        # Mock the DB path in config or where it's used
        # Since DoctorMatcher reads from config.DOCTORS_DB_PATH, we might need to patch it or the class
        
        # For this test, let's just instantiate and manually set the df if possible, 
        # or better, patch pd.read_csv
        
        df = pd.DataFrame({
            'full_name': ['Dr. A', 'Dr. B'],
            'specialty': ['Dentist', 'Cardiologist'],
            'primary_symptoms': ['tooth pain', 'chest pain'],
            'exclude_keywords': ['', 'tooth'],
            'secondary_symptoms': ['', ''],
            'Keywords': ['', '']
        })
        
        matcher = DoctorMatcher()
        matcher.doctors_df = df
        
        # Test exact match
        matches = matcher.find_doctors(['tooth pain'], specialty='Dentist')
        assert len(matches) == 1
        assert matches[0]['doctor']['full_name'] == 'Dr. A'
        
        # Test exclude logic (Cardiologist excludes 'tooth')
        matches = matcher.find_doctors(['tooth pain'], specialty='Cardiologist')
        assert len(matches) == 1
        assert matches[0]['doctor']['full_name'] == 'Dr. A'

    def test_format_doctor_card(self):
        matcher = DoctorMatcher()
        doctor = {
            'full_name': 'Dr. Test',
            'specialty': 'General',
            'clinic_name': 'Test Clinic',
            'address': '123 St',
            'phone_number': '555-5555',
            'primary_symptoms': 'cough, cold'
        }
        match = {'doctor': doctor, 'score': 10}
        card = matcher.format_doctor_card(match)
        assert 'Dr. Test' in card
        assert 'Test Clinic' in card
        assert 'Cough' in card
