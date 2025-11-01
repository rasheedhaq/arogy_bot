"""
Test longer conversations with the bot
This simulates extended patient-doctor conversations
"""
import asyncio
from bot_intelligent import get_doctor_response
import json

async def test_long_conversation_fever():
    """Test a complete fever consultation flow"""
    print("\n" + "="*80)
    print("🧪 TEST: Complete Fever Consultation (Long Conversation)")
    print("="*80)
    
    conversation_history = []
    
    # Turn 1
    print("\n[Turn 1]")
    print("👤 Patient: I have fever")
    response = await get_doctor_response("I have fever", conversation_history)
    print(f"🤖 Doctor: {response['message']}")
    print(f"Ready: {response['ready_for_recommendation']}")
    
    if not response['ready_for_recommendation']:
        # Turn 2
        print("\n[Turn 2]")
        print("👤 Patient: 102F since yesterday")
        response = await get_doctor_response("102F since yesterday", conversation_history)
        print(f"🤖 Doctor: {response['message']}")
        print(f"Ready: {response['ready_for_recommendation']}")
    
    if not response['ready_for_recommendation']:
        # Turn 3
        print("\n[Turn 3]")
        print("👤 Patient: also have headache and body pain")
        response = await get_doctor_response("also have headache and body pain", conversation_history)
        print(f"🤖 Doctor: {response['message']}")
        print(f"Ready: {response['ready_for_recommendation']}")
    
    if not response['ready_for_recommendation']:
        # Turn 4
        print("\n[Turn 4]")
        print("👤 Patient: feeling very weak")
        response = await get_doctor_response("feeling very weak", conversation_history)
        print(f"🤖 Doctor: {response['message']}")
        print(f"Ready: {response['ready_for_recommendation']}")
    
    if response['ready_for_recommendation']:
        print("\n✅ SUCCESS: Bot ready to recommend doctor")
        if 'recommended_doctor' in response:
            print(f"👨‍⚕️ Recommended: {response['recommended_doctor']}")
    else:
        print("\n⚠️ Note: Bot still gathering information")

async def test_long_conversation_toothache():
    """Test a complete toothache consultation flow"""
    print("\n" + "="*80)
    print("🧪 TEST: Complete Toothache Consultation (Long Conversation)")
    print("="*80)
    
    conversation_history = []
    
    # Turn 1
    print("\n[Turn 1]")
    print("👤 Patient: tooth pain")
    response = await get_doctor_response("tooth pain", conversation_history)
    print(f"🤖 Doctor: {response['message']}")
    print(f"Ready: {response['ready_for_recommendation']}")
    
    if not response['ready_for_recommendation']:
        # Turn 2
        print("\n[Turn 2]")
        print("👤 Patient: very severe, can't eat")
        response = await get_doctor_response("very severe, can't eat", conversation_history)
        print(f"🤖 Doctor: {response['message']}")
        print(f"Ready: {response['ready_for_recommendation']}")
    
    if not response['ready_for_recommendation']:
        # Turn 3
        print("\n[Turn 3]")
        print("👤 Patient: 3 days now, gums are swollen")
        response = await get_doctor_response("3 days now, gums are swollen", conversation_history)
        print(f"🤖 Doctor: {response['message']}")
        print(f"Ready: {response['ready_for_recommendation']}")
    
    if not response['ready_for_recommendation']:
        # Turn 4
        print("\n[Turn 4]")
        print("👤 Patient: sometimes bleeding from gums")
        response = await get_doctor_response("sometimes bleeding from gums", conversation_history)
        print(f"🤖 Doctor: {response['message']}")
        print(f"Ready: {response['ready_for_recommendation']}")
    
    if response['ready_for_recommendation']:
        print("\n✅ SUCCESS: Bot ready to recommend doctor")
        if 'recommended_doctor' in response:
            print(f"👨‍⚕️ Recommended: {response['recommended_doctor']}")

async def test_long_conversation_pregnancy():
    """Test a complete pregnancy consultation flow"""
    print("\n" + "="*80)
    print("🧪 TEST: Complete Pregnancy Consultation (Long Conversation)")
    print("="*80)
    
    conversation_history = []
    
    # Turn 1
    print("\n[Turn 1]")
    print("👤 Patient: I think I'm pregnant")
    response = await get_doctor_response("I think I'm pregnant", conversation_history)
    print(f"🤖 Doctor: {response['message']}")
    print(f"Ready: {response['ready_for_recommendation']}")
    
    if not response['ready_for_recommendation']:
        # Turn 2
        print("\n[Turn 2]")
        print("👤 Patient: missed my period, feeling nauseous")
        response = await get_doctor_response("missed my period, feeling nauseous", conversation_history)
        print(f"🤖 Doctor: {response['message']}")
        print(f"Ready: {response['ready_for_recommendation']}")
    
    if not response['ready_for_recommendation']:
        # Turn 3
        print("\n[Turn 3]")
        print("👤 Patient: home test was positive")
        response = await get_doctor_response("home test was positive", conversation_history)
        print(f"🤖 Doctor: {response['message']}")
        print(f"Ready: {response['ready_for_recommendation']}")
    
    if response['ready_for_recommendation']:
        print("\n✅ SUCCESS: Bot ready to recommend doctor")
        if 'recommended_doctor' in response:
            print(f"👨‍⚕️ Recommended: {response['recommended_doctor']}")

async def test_edge_case_gibberish_then_real():
    """Test edge case: gibberish followed by real symptoms"""
    print("\n" + "="*80)
    print("🧪 TEST: Edge Case - Gibberish Then Real Complaint")
    print("="*80)
    
    conversation_history = []
    
    # Turn 1 - Gibberish
    print("\n[Turn 1]")
    print("👤 Patient: ggg,ggg,hhh")
    response = await get_doctor_response("ggg,ggg,hhh", conversation_history)
    print(f"🤖 Doctor: {response['message']}")
    
    # Turn 2 - More gibberish
    print("\n[Turn 2]")
    print("👤 Patient: jjjjkkkk")
    response = await get_doctor_response("jjjjkkkk", conversation_history)
    print(f"🤖 Doctor: {response['message']}")
    
    # Turn 3 - Real complaint
    print("\n[Turn 3]")
    print("👤 Patient: actually I have severe headache")
    response = await get_doctor_response("actually I have severe headache", conversation_history)
    print(f"🤖 Doctor: {response['message']}")
    print(f"Ready: {response['ready_for_recommendation']}")
    
    if not response['ready_for_recommendation']:
        # Turn 4
        print("\n[Turn 4]")
        print("👤 Patient: for 2 days, very painful")
        response = await get_doctor_response("for 2 days, very painful", conversation_history)
        print(f"🤖 Doctor: {response['message']}")
        print(f"Ready: {response['ready_for_recommendation']}")
    
    print("\n✅ Test completed")

async def test_emergency_recognition():
    """Test if bot recognizes emergency situations"""
    print("\n" + "="*80)
    print("🧪 TEST: Emergency Recognition")
    print("="*80)
    
    conversation_history = []
    
    print("\n[Turn 1]")
    print("👤 Patient: severe chest pain and difficulty breathing")
    response = await get_doctor_response("severe chest pain and difficulty breathing", conversation_history)
    print(f"🤖 Doctor: {response['message']}")
    print(f"🚨 Severity: {response.get('severity', 'N/A')}")
    print(f"Ready: {response['ready_for_recommendation']}")
    
    if 'emergency' in response['message'].lower() or 'urgent' in response['message'].lower() or '112' in response['message']:
        print("\n✅ SUCCESS: Bot recognized emergency situation")
    else:
        print("\n⚠️ Note: Bot may need better emergency detection")

async def main():
    """Run all long conversation tests"""
    print("\n" + "="*80)
    print("🧪 LONG CONVERSATION TESTS")
    print("Testing extended patient-doctor interactions")
    print("="*80)
    
    try:
        await test_long_conversation_fever()
        await asyncio.sleep(1)
        
        await test_long_conversation_toothache()
        await asyncio.sleep(1)
        
        await test_long_conversation_pregnancy()
        await asyncio.sleep(1)
        
        await test_edge_case_gibberish_then_real()
        await asyncio.sleep(1)
        
        await test_emergency_recognition()
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("✅ ALL LONG CONVERSATION TESTS COMPLETED")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
