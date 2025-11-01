"""
Test script for intelligent bot - simulates conversations
Tests various scenarios to validate LLM-driven dialogue
"""
import asyncio
import json
from bot_intelligent import get_doctor_response


async def test_conversation(scenario_name, messages):
    """
    Test a complete conversation scenario
    
    Args:
        scenario_name: Name of the test scenario
        messages: List of patient messages to simulate
    """
    print(f"\n{'='*80}")
    print(f"🧪 TEST SCENARIO: {scenario_name}")
    print(f"{'='*80}\n")
    
    conversation_history = []
    collected_info = {}
    
    for i, patient_msg in enumerate(messages, 1):
        print(f"\n👤 PATIENT (Message {i}): {patient_msg}")
        
        # Add to history
        conversation_history.append({
            "role": "patient",
            "message": patient_msg
        })
        
        # Build context
        conversation_context = "\n".join([
            f"{'Patient' if msg['role'] == 'patient' else 'Doctor'}: {msg['message']}"
            for msg in conversation_history
        ])
        
        # Get doctor's response
        try:
            response = await get_doctor_response(conversation_context, collected_info)
            
            print(f"\n🤖 DOCTOR RESPONSE:")
            print(f"   Message: {response['message']}")
            print(f"   Ready for recommendation: {response.get('ready_for_recommendation', False)}")
            
            if response.get('extracted_info'):
                print(f"   Extracted info: {json.dumps(response['extracted_info'], indent=6)}")
                collected_info.update(response['extracted_info'])
            
            if response.get('specialty'):
                print(f"   Specialty: {response['specialty']}")
                print(f"   Symptoms: {response.get('symptoms', [])}")
            
            if response.get('reasoning'):
                print(f"   Reasoning: {response['reasoning']}")
            
            # Add doctor response to history
            conversation_history.append({
                "role": "doctor",
                "message": response['message']
            })
            
            # Check if conversation completed
            if response.get('ready_for_recommendation'):
                print(f"\n✅ CONVERSATION COMPLETED")
                print(f"   Final Specialty: {response.get('specialty')}")
                print(f"   Symptoms Identified: {response.get('symptoms')}")
                break
                
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            break
    
    print(f"\n{'='*80}")
    print(f"FINAL COLLECTED INFO:")
    print(json.dumps(collected_info, indent=2))
    print(f"{'='*80}\n")


async def main():
    """Run all test scenarios"""
    
    print("\n" + "="*80)
    print("🚀 AROGYAMITRA INTELLIGENT BOT - TEST SUITE")
    print("="*80)
    
    # Test 1: Simple short complaint (should ask follow-up questions)
    await test_conversation(
        "Test 1: Simple Complaint - Tooth Pain",
        [
            "tooth pain",
            "3 days",
            "it's severe, like 8 out of 10",
            "yes, swelling in my jaw"
        ]
    )
    
    # Test 2: Detailed complaint (should get recommendation quickly)
    await test_conversation(
        "Test 2: Detailed Complaint - Immediate Analysis",
        [
            "I have severe tooth pain for the past 3 days with swelling in my jaw. It hurts when I eat.",
        ]
    )
    
    # Test 3: Chest pain (emergency scenario)
    await test_conversation(
        "Test 3: Emergency - Chest Pain",
        [
            "I'm having chest pain",
            "started this morning, about 4 hours ago",
            "it's very severe, 9 out of 10",
            "yes, I feel breathless and sweating a lot"
        ]
    )
    
    # Test 4: Vague initial complaint
    await test_conversation(
        "Test 4: Vague Complaint - Not Feeling Well",
        [
            "I'm not feeling well",
            "stomach pain and nausea",
            "2 days",
            "moderate, around 5",
        ]
    )
    
    # Test 5: Child's fever
    await test_conversation(
        "Test 5: Pediatric Case - Fever",
        [
            "my child has fever",
            "102°F for 2 days",
            "cough and runny nose",
            "3 years old"
        ]
    )
    
    # Test 6: Single detailed message (ultimate intelligence test)
    await test_conversation(
        "Test 6: Single Message - Complete Info",
        [
            "My 5 year old daughter has high fever of 103°F since yesterday with cough and difficulty breathing. She's also vomiting.",
        ]
    )
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
