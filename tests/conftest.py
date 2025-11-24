import pytest
import sys
import os
from unittest.mock import MagicMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def mock_doctors_csv(tmp_path):
    """Create a temporary CSV file for doctor data"""
    d = tmp_path / "data"
    d.mkdir()
    p = d / "doctors_test.csv"
    p.write_text("full_name,specialty,primary_symptoms,exclude_keywords\nDr. Test,General Physician,fever,surgery")
    return str(p)

@pytest.fixture
def mock_llm_response():
    """Mock LLM response"""
    return {
        "message": "Test message",
        "ready_for_recommendation": False,
        "extracted_info": {}
    }
