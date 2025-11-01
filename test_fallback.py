"""
Quick test to verify multi-provider fallback works
Tests 10 scenarios to validate Gemini fallback when Groq rate limit hits
"""
import asyncio
import json
from llm_client import LLMClient

# Initialize LLM client
llm_client = LLMClient()


async def get_doctor_response(conversation_context: str, collected_info: dict):
    """
    Standalone version of doctor response for testing
    LLM acts as a medical doctor to decide next question or recommendation
    """
    system_prompt = """You are an experienced medical doctor conducting a patient consultation via chat.
    
    Your goals:
    1. Gather essential information naturally (chief complaint, duration, severity, associated symptoms, relevant medical history)
    2. Ask ONE question at a time, like a real doctor would
    3. Be empathetic, professional, and conversational
    4. Once you have enough information, provide a specialty recommendation
    
    IMPORTANT: After 3-4 exchanges, you MUST have enough information to make a recommendation.
    
    RESPONSE FORMAT (JSON):
    {
        "message": "Your question or final assessment to the patient",
        "ready_for_recommendation": false,
        "extracted_info": {
            "chief_complaint": "extracted symptom",
            "duration": "how long",
            "severity": "mild/moderate/severe",
            "associated_symptoms": ["symptom1", "symptom2"]
        },
        "specialty": "Exact specialty name when ready (Dentist, Cardiologist, Pediatrician, etc.)",
        "symptoms": ["symptom1", "symptom2"]
    }
    """
    
    user_prompt = f"""CONVERSATION SO FAR:
{conversation_context}

INFORMATION COLLECTED:
{json.dumps(collected_info, indent=2)}

Based on this conversation, decide what to do next."""
    
    try:
        # Use the fallback-enabled chat method
        response_text = llm_client.chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=800,
            json_mode=True
        )
        
        if not response_text:
            raise Exception("No response from LLM (all providers failed)")
        
        result = json.loads(response_text)
        return result
        
    except Exception as e:
        print(f"Error in get_doctor_response: {str(e)}")
        raise


async def test_conversation(scenario_name: str, messages: list):
    """Test a complete conversation scenario"""
    print(f"\n{'='*80}")
    print(f"🧪 {scenario_name}")
    print(f"{'='*80}\n")
    
    conversation_history = []
    collected_info = {}
    
    for i, patient_msg in enumerate(messages, 1):
        print(f"👤 Patient: {patient_msg}")
        
        conversation_history.append({
            "role": "patient",
            "message": patient_msg
        })
        
        conversation_context = "\n".join([
            f"{'Patient' if msg['role'] == 'patient' else 'Doctor'}: {msg['message']}"
            for msg in conversation_history
        ])
        
        try:
            response = await get_doctor_response(conversation_context, collected_info)
            
            print(f"🤖 Doctor: {response['message']}\n")
            
            if response.get('extracted_info'):
                collected_info.update(response['extracted_info'])
            
            conversation_history.append({
                "role": "doctor",
                "message": response['message']
            })
            
            if response.get('ready_for_recommendation'):
                print(f"✅ COMPLETED - Specialty: {response.get('specialty')}, Symptoms: {response.get('symptoms')}")
                break
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            break


async def main():
    """Run 10 quick test scenarios"""
    
    print("\n" + "="*80)
    print("🚀 MULTI-PROVIDER FALLBACK TEST - 10 Quick Scenarios")
    print("="*80 + "\n")
    
    # Test 1: Edge case - Gibberish
    await test_conversation(
        "Test 1: EDGE - Kid typing gibberish",
        ["ggg,ggg,hhh", "jjjjkkkk", "tooth hurts", "3 days"]
    )
    
    # Test 2: Simple complaint
    await test_conversation(
        "Test 2: Simple fever",
        ["I have fever", "since yesterday", "101°F", "body pain"]
    )
    
    # Test 3: Emergency
    await test_conversation(
        "Test 3: EMERGENCY - Chest pain",
        ["severe chest pain", "started 1 hour ago", "9/10 pain", "sweating"]
    )
    
    # Test 4: Pediatric
    await test_conversation(
        "Test 4: Baby fever",
        ["my 6 month old baby has fever", "103°F", "crying a lot"]
    )
    
    # Test 5: Detailed single message
    await test_conversation(
        "Test 5: Detailed complaint",
        ["I have severe tooth pain for the past 3 days with swelling in my jaw"]
    )
    
    # Test 6: Vague
    await test_conversation(
        "Test 6: Vague complaint",
        ["not feeling well", "stomach", "2 days", "moderate"]
    )
    
    # Test 7: Women's health
    await test_conversation(
        "Test 7: PCOD symptoms",
        ["irregular periods and weight gain", "6 months", "also hair growth"]
    )
    
    # Test 8: Ortho
    await test_conversation(
        "Test 8: Knee pain",
        ["knee pain when walking", "2 weeks", "swelling"]
    )
    
    # Test 9: ENT
    await test_conversation(
        "Test 9: Ear pain",
        ["severe ear pain", "right ear", "can't sleep"]
    )
    
    # Test 10: Edge - Patient says no
    await test_conversation(
        "Test 10: EDGE - Patient says no",
        ["headache", "no", "no", "ok it's severe"]
    )
    
    print("\n" + "="*80)
    print("✅ QUICK TEST COMPLETED")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
