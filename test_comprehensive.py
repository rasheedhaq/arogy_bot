"""
Comprehensive Test Suite for Arogyamitra Intelligent Bot
Tests 100+ scenarios including:
- All 19 doctors in database
- Edge cases (no/nonsense responses)
- Emergency scenarios
- Pediatric cases
- Women's health
- Oncology cases
- Orthopedics & sports injuries
- Random gibberish inputs
- Uncooperative patients
"""
import asyncio
import json
from typing import List, Dict
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
    Set "ready_for_recommendation": true when you have:
    1. Chief complaint identified
    2. Duration known (even if approximate)
    3. Severity assessed (even if patient described it loosely)
    4. Key associated symptoms noted
    
    Don't over-ask! Real doctors make decisions with limited info.
    
    EDGE CASES HANDLING:
    - If patient gives gibberish/nonsense (like "ggg", "hhh", random characters): Politely ask them to describe their issue
    - If patient says only "no": Try to rephrase your question or ask differently
    - If patient is uncooperative after 3 attempts: Make best guess recommendation
    - If patient gives one-word vague answers: Guide them with specific options
    
    RESPONSE FORMAT (JSON):
    {
        "message": "Your question or final assessment to the patient",
        "ready_for_recommendation": false,
        "extracted_info": {
            "chief_complaint": "extracted symptom",
            "duration": "how long",
            "severity": "mild/moderate/severe",
            "associated_symptoms": ["symptom1", "symptom2"],
            "red_flags": ["emergency indicator if any"]
        },
        "specialty": "Exact specialty name when ready (Dentist, Cardiologist, Pediatrician, etc.)",
        "symptoms": ["symptom1", "symptom2"],
        "reasoning": "Brief explanation of your decision"
    }
    """
    
    user_prompt = f"""CONVERSATION SO FAR:
{conversation_context}

INFORMATION COLLECTED:
{json.dumps(collected_info, indent=2)}

Based on this conversation, decide:
1. If you need more information: Ask the next question
2. If you have enough: Provide specialty recommendation and set ready_for_recommendation=true

Remember: After 3-4 exchanges, you should have enough to recommend a specialty!"""
    
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


class TestResults:
    """Track test results"""
    def __init__(self):
        self.total = 0
        self.completed = 0
        self.incomplete = 0
        self.errors = 0
        self.edge_cases_handled = 0
        self.details = []
    
    def add_result(self, scenario: str, completed: bool, specialty: str = None, exchanges: int = 0, error: str = None):
        self.total += 1
        if error:
            self.errors += 1
        elif completed:
            self.completed += 1
        else:
            self.incomplete += 1
        
        self.details.append({
            "scenario": scenario,
            "completed": completed,
            "specialty": specialty,
            "exchanges": exchanges,
            "error": error
        })
    
    def print_summary(self):
        print("\n" + "="*100)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("="*100)
        print(f"\n📈 STATISTICS:")
        print(f"   Total Tests: {self.total}")
        print(f"   ✅ Completed: {self.completed} ({self.completed/self.total*100:.1f}%)")
        print(f"   ⏳ Incomplete: {self.incomplete} ({self.incomplete/self.total*100:.1f}%)")
        print(f"   ❌ Errors: {self.errors} ({self.errors/self.total*100:.1f}%)")
        
        print(f"\n🎯 SPECIALTY DISTRIBUTION:")
        specialties = {}
        for detail in self.details:
            if detail['specialty']:
                specialties[detail['specialty']] = specialties.get(detail['specialty'], 0) + 1
        
        for specialty, count in sorted(specialties.items(), key=lambda x: x[1], reverse=True):
            print(f"   {specialty}: {count} cases")
        
        print(f"\n💡 EDGE CASES:")
        edge_cases = [d for d in self.details if any(keyword in d['scenario'].lower() for keyword in ['gibberish', 'no', 'uncooperative', 'emoji', 'empty'])]
        print(f"   Edge cases tested: {len(edge_cases)}")
        print(f"   Edge cases completed: {sum(1 for d in edge_cases if d['completed'])}")
        
        print("\n" + "="*100 + "\n")


results = TestResults()


async def test_conversation(scenario_name: str, messages: List[str], max_exchanges: int = 6, silent: bool = False):
    """
    Test a complete conversation scenario
    
    Args:
        scenario_name: Name of the test scenario
        messages: List of patient messages to simulate
        max_exchanges: Maximum number of exchanges before stopping
        silent: If True, don't print detailed output
    """
    if not silent:
        print(f"\n{'='*100}")
        print(f"🧪 {scenario_name}")
        print(f"{'='*100}\n")
    
    conversation_history = []
    collected_info = {}
    exchanges = 0
    completed = False
    specialty = None
    error_msg = None
    
    for i, patient_msg in enumerate(messages, 1):
        if exchanges >= max_exchanges:
            break
            
        if not silent:
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
            exchanges += 1
            
            if not silent:
                print(f"🤖 Doctor: {response['message']}\n")
            
            if response.get('extracted_info'):
                collected_info.update(response['extracted_info'])
            
            conversation_history.append({
                "role": "doctor",
                "message": response['message']
            })
            
            if response.get('ready_for_recommendation'):
                completed = True
                specialty = response.get('specialty')
                if not silent:
                    print(f"✅ COMPLETED - Specialty: {specialty}, Symptoms: {response.get('symptoms')}")
                break
                
        except Exception as e:
            error_msg = str(e)
            if not silent:
                print(f"❌ ERROR: {error_msg}")
            break
    
    if not completed and not error_msg and not silent:
        print(f"⏳ INCOMPLETE after {exchanges} exchanges")
    
    results.add_result(scenario_name, completed, specialty, exchanges, error_msg)


async def main():
    """Run all 100+ test scenarios"""
    
    print("\n" + "="*100)
    print("🚀 AROGYAMITRA COMPREHENSIVE TEST SUITE - 100+ SCENARIOS")
    print("="*100 + "\n")
    
    # ============================================================
    # SECTION 1: EDGE CASES - Uncooperative/Nonsense Inputs (15 tests)
    # ============================================================
    print("\n🔥 SECTION 1: EDGE CASES - Testing Bot Resilience\n")
    
    await test_conversation(
        "EDGE-1: Patient says 'no' repeatedly",
        ["tooth pain", "no", "no", "no", "no"]
    )
    
    await test_conversation(
        "EDGE-2: Kid typing gibberish",
        ["ggg,ggg,hhh", "jjjjkkkk", "mmmmm"]
    )
    
    await test_conversation(
        "EDGE-3: Random characters",
        ["asdfghjkl", "qwertyuiop", "zxcvbnm"]
    )
    
    await test_conversation(
        "EDGE-4: Numbers only",
        ["123456", "999", "0000"]
    )
    
    await test_conversation(
        "EDGE-5: Single character responses",
        ["pain", "a", "b", "c", "d"]
    )
    
    await test_conversation(
        "EDGE-6: Emoji spam",
        ["😀😀😀", "🤔🤔", "😭😭😭"]
    )
    
    await test_conversation(
        "EDGE-7: Empty/whitespace",
        ["headache", "   ", "", "  "]
    )
    
    await test_conversation(
        "EDGE-8: Mixed gibberish with real complaint",
        ["tooth pain very bad", "hhhhh", "ggggg", "ok it hurts when I eat"]
    )
    
    await test_conversation(
        "EDGE-9: Patient changes mind",
        ["headache", "actually no, stomach pain", "wait, it's chest pain"]
    )
    
    await test_conversation(
        "EDGE-10: Vague one-word answers",
        ["sick", "yes", "bad", "ok"]
    )
    
    await test_conversation(
        "EDGE-11: Patient asks questions instead",
        ["what should I do?", "do I need medicine?", "is this serious?"]
    )
    
    await test_conversation(
        "EDGE-12: All caps shouting",
        ["HELP ME!!!", "IT HURTS SO MUCH!!!", "EMERGENCY!!!"]
    )
    
    await test_conversation(
        "EDGE-13: Multiple languages mixed",
        ["head novu", "വേദന", "pain"]
    )
    
    await test_conversation(
        "EDGE-14: Patient refuses to answer",
        ["I don't want to say", "none of your business", "why do you ask?"]
    )
    
    await test_conversation(
        "EDGE-15: Repetitive complaints",
        ["pain pain pain", "hurts hurts", "bad bad bad"]
    )
    
    # ============================================================
    # SECTION 2: GENERAL PHYSICIAN - Dr. Mohammed Ali (8 tests)
    # ============================================================
    print("\n🩺 SECTION 2: GENERAL PHYSICIAN Cases\n")
    
    await test_conversation(
        "GP-1: Simple fever",
        ["I have fever", "since yesterday", "101°F", "body pain and headache"],
        silent=True
    )
    
    await test_conversation(
        "GP-2: Cold and cough",
        ["bad cold with cough", "3 days", "moderate", "runny nose and sneezing"],
        silent=True
    )
    
    await test_conversation(
        "GP-3: Viral flu symptoms",
        ["flu symptoms - fever, body pain, weakness", "2 days"],
        silent=True
    )
    
    await test_conversation(
        "GP-4: General checkup request",
        ["I want a general health checkup", "no specific complaints", "routine check"],
        silent=True
    )
    
    await test_conversation(
        "GP-5: Headache simple",
        ["headache", "since morning", "mild to moderate"],
        silent=True
    )
    
    await test_conversation(
        "GP-6: Body pain without fever",
        ["body pain all over", "started yesterday", "no fever"],
        silent=True
    )
    
    await test_conversation(
        "GP-7: Persistent cough no fever",
        ["cough for 5 days", "dry cough", "no fever or cold"],
        silent=True
    )
    
    await test_conversation(
        "GP-8: Fatigue and weakness",
        ["feeling very weak and tired", "for a week now", "no energy"],
        silent=True
    )
    
    # ============================================================
    # SECTION 3: GYNAECOLOGIST - Dr. Fathima Suhail (8 tests)
    # ============================================================
    print("\n👩 SECTION 3: GYNAECOLOGY Cases\n")
    
    await test_conversation(
        "GYNAE-1: Pregnancy confirmation",
        ["I think I'm pregnant", "missed period", "yes, tested positive"],
        silent=True
    )
    
    await test_conversation(
        "GYNAE-2: PCOD symptoms",
        ["irregular periods and weight gain", "6 months", "also hair growth on face"],
        silent=True
    )
    
    await test_conversation(
        "GYNAE-3: Menstrual cramps",
        ["severe period pain", "every month", "8 out of 10 pain"],
        silent=True
    )
    
    await test_conversation(
        "GYNAE-4: Pregnancy complications",
        ["I'm 6 months pregnant and have bleeding", "started today"],
        silent=True
    )
    
    await test_conversation(
        "GYNAE-5: Maternity consultation",
        ["first pregnancy, need prenatal care", "8 weeks pregnant"],
        silent=True
    )
    
    await test_conversation(
        "GYNAE-6: Irregular periods",
        ["my periods are very irregular", "sometimes skip months", "no other symptoms"],
        silent=True
    )
    
    await test_conversation(
        "GYNAE-7: Pelvic pain",
        ["lower abdominal pain", "for 2 weeks", "not related to periods"],
        silent=True
    )
    
    await test_conversation(
        "GYNAE-8: Women's health checkup",
        ["want annual women's health screening", "no complaints"],
        silent=True
    )
    
    # ============================================================
    # SECTION 4: CARDIOLOGY - Dr. Sreejith Namboothiri (10 tests)
    # ============================================================
    print("\n❤️ SECTION 4: CARDIOLOGY Cases\n")
    
    await test_conversation(
        "CARDIO-1: Chest pain emergency",
        ["severe chest pain", "started 1 hour ago", "9/10 pain", "sweating and breathless"],
        silent=True
    )
    
    await test_conversation(
        "CARDIO-2: High blood pressure",
        ["my BP is 160/100", "headache and dizziness", "for 2 days"],
        silent=True
    )
    
    await test_conversation(
        "CARDIO-3: Heart palpitations",
        ["heart racing and pounding", "happens frequently", "feels scary"],
        silent=True
    )
    
    await test_conversation(
        "CARDIO-4: Suspected heart attack",
        ["crushing chest pain radiating to left arm", "sweating profusely", "very severe"],
        silent=True
    )
    
    await test_conversation(
        "CARDIO-5: High cholesterol follow-up",
        ["my cholesterol is 250", "want treatment", "family history of heart disease"],
        silent=True
    )
    
    await test_conversation(
        "CARDIO-6: Hypertension management",
        ["diagnosed with hypertension", "need medication adjustment"],
        silent=True
    )
    
    await test_conversation(
        "CARDIO-7: Chest discomfort after exercise",
        ["chest tightness when I walk upstairs", "goes away with rest"],
        silent=True
    )
    
    await test_conversation(
        "CARDIO-8: Irregular heartbeat",
        ["my heart skips beats sometimes", "noticed for a month"],
        silent=True
    )
    
    await test_conversation(
        "CARDIO-9: Shortness of breath",
        ["getting breathless even with little activity", "for 2 weeks"],
        silent=True
    )
    
    await test_conversation(
        "CARDIO-10: Cardiac checkup request",
        ["I'm 50 years old, want heart checkup", "no complaints but family history"],
        silent=True
    )
    
    # ============================================================
    # SECTION 5: DERMATOLOGY - Dr. Ramya Sadanandan (7 tests)
    # ============================================================
    print("\n🧴 SECTION 5: DERMATOLOGY Cases\n")
    
    await test_conversation(
        "DERM-1: Skin rash",
        ["red itchy rash on my arms", "started 3 days ago", "spreading"],
        silent=True
    )
    
    await test_conversation(
        "DERM-2: Acne problem",
        ["severe acne on face", "for months", "nothing helps"],
        silent=True
    )
    
    await test_conversation(
        "DERM-3: Eczema flare",
        ["dry scaly patches on skin", "very itchy", "had this before"],
        silent=True
    )
    
    await test_conversation(
        "DERM-4: Hair loss",
        ["losing a lot of hair", "for 2 months", "bald patches forming"],
        silent=True
    )
    
    await test_conversation(
        "DERM-5: Skin allergy",
        ["skin is red and swollen", "after using new soap", "burning sensation"],
        silent=True
    )
    
    await test_conversation(
        "DERM-6: Psoriasis concern",
        ["thick scaly skin patches", "silvery scales", "on elbows and knees"],
        silent=True
    )
    
    await test_conversation(
        "DERM-7: Severe itching",
        ["unbearable itching all over body", "worse at night", "no visible rash"],
        silent=True
    )
    
    # ============================================================
    # SECTION 6: ORTHOPEDICS - Multiple Doctors (10 tests)
    # ============================================================
    print("\n🦴 SECTION 6: ORTHOPEDICS Cases\n")
    
    await test_conversation(
        "ORTHO-1: Knee pain",
        ["knee pain when walking", "for 2 weeks", "swelling"],
        silent=True
    )
    
    await test_conversation(
        "ORTHO-2: Back pain",
        ["severe lower back pain", "can't bend", "3 days"],
        silent=True
    )
    
    await test_conversation(
        "ORTHO-3: Fracture suspected",
        ["fell down, ankle very painful", "can't put weight", "swollen"],
        silent=True
    )
    
    await test_conversation(
        "ORTHO-4: Sports injury - ACL",
        ["knee gave out while playing football", "heard a pop sound", "very unstable"],
        silent=True
    )
    
    await test_conversation(
        "ORTHO-5: Shoulder pain",
        ["can't lift arm above head", "shoulder pain", "for a month"],
        silent=True
    )
    
    await test_conversation(
        "ORTHO-6: Arthritis symptoms",
        ["joint pain in multiple joints", "morning stiffness", "I'm 65 years old"],
        silent=True
    )
    
    await test_conversation(
        "ORTHO-7: Neck pain",
        ["stiff neck, can't turn head", "since yesterday"],
        silent=True
    )
    
    await test_conversation(
        "ORTHO-8: Hip pain elderly",
        ["hip pain when walking", "70 years old", "difficulty getting up"],
        silent=True
    )
    
    await test_conversation(
        "ORTHO-9: Bone pain general",
        ["bone pain in legs", "no injury", "for weeks"],
        silent=True
    )
    
    await test_conversation(
        "ORTHO-10: Spine injury",
        ["back injury from lifting heavy object", "sharp pain", "can't stand straight"],
        silent=True
    )
    
    # ============================================================
    # SECTION 7: PEDIATRICS - Dr. Shaji P S (8 tests)
    # ============================================================
    print("\n👶 SECTION 7: PEDIATRICS Cases\n")
    
    await test_conversation(
        "PEDS-1: Baby fever",
        ["my 6 month old baby has fever", "103°F", "crying a lot"],
        silent=True
    )
    
    await test_conversation(
        "PEDS-2: Vaccination due",
        ["my child needs vaccination", "2 months old"],
        silent=True
    )
    
    await test_conversation(
        "PEDS-3: Child cough and cold",
        ["my 3 year old has bad cough", "for 4 days", "fever also"],
        silent=True
    )
    
    await test_conversation(
        "PEDS-4: Infant not feeding",
        ["newborn not feeding well", "10 days old", "vomiting"],
        silent=True
    )
    
    await test_conversation(
        "PEDS-5: Child stomach pain",
        ["my 8 year old has stomach pain", "vomiting", "since morning"],
        silent=True
    )
    
    await test_conversation(
        "PEDS-6: Rash on baby",
        ["red spots all over baby's body", "with fever", "6 months old"],
        silent=True
    )
    
    await test_conversation(
        "PEDS-7: Child not gaining weight",
        ["my 1 year old not gaining weight", "feeding issues"],
        silent=True
    )
    
    await test_conversation(
        "PEDS-8: Breathing difficulty child",
        ["my 5 year old breathing fast", "wheezing sound", "fever"],
        silent=True
    )
    
    # ============================================================
    # SECTION 8: GASTROENTEROLOGY - Dr. Abdul Gafoor (8 tests)
    # ============================================================
    print("\n🍽️ SECTION 8: GASTROENTEROLOGY Cases\n")
    
    await test_conversation(
        "GASTRO-1: Severe acidity",
        ["burning sensation in chest", "after eating", "for weeks"],
        silent=True
    )
    
    await test_conversation(
        "GASTRO-2: Stomach ulcer pain",
        ["sharp stomach pain", "on empty stomach", "relieved by eating"],
        silent=True
    )
    
    await test_conversation(
        "GASTRO-3: Diarrhea persistent",
        ["loose motions for 3 days", "dehydrated", "stomach cramps"],
        silent=True
    )
    
    await test_conversation(
        "GASTRO-4: Jaundice symptoms",
        ["yellow eyes and skin", "dark urine", "weakness"],
        silent=True
    )
    
    await test_conversation(
        "GASTRO-5: Gas and bloating",
        ["severe gas problem", "bloated stomach", "uncomfortable"],
        silent=True
    )
    
    await test_conversation(
        "GASTRO-6: Liver problem suspected",
        ["abdominal pain right side", "fatigue", "loss of appetite"],
        silent=True
    )
    
    await test_conversation(
        "GASTRO-7: Indigestion chronic",
        ["always feel heavy after eating", "nausea", "for months"],
        silent=True
    )
    
    await test_conversation(
        "GASTRO-8: Abdominal pain severe",
        ["severe stomach pain", "can't eat", "vomiting"],
        silent=True
    )
    
    # ============================================================
    # SECTION 9: ENT - Dr. Anoop Kumar (7 tests)
    # ============================================================
    print("\n👂 SECTION 9: ENT Cases\n")
    
    await test_conversation(
        "ENT-1: Ear pain",
        ["severe ear pain", "right ear", "can't sleep"],
        silent=True
    )
    
    await test_conversation(
        "ENT-2: Sore throat",
        ["very painful throat", "can't swallow", "fever also"],
        silent=True
    )
    
    await test_conversation(
        "ENT-3: Sinus infection",
        ["blocked nose and headache", "pressure in face", "for a week"],
        silent=True
    )
    
    await test_conversation(
        "ENT-4: Tonsillitis",
        ["swollen tonsils", "white patches in throat", "painful"],
        silent=True
    )
    
    await test_conversation(
        "ENT-5: Hearing loss",
        ["can't hear well from left ear", "for months"],
        silent=True
    )
    
    await test_conversation(
        "ENT-6: Vertigo",
        ["room spinning", "dizziness", "nausea"],
        silent=True
    )
    
    await test_conversation(
        "ENT-7: Nose block chronic",
        ["nose always blocked", "breathing difficulty", "for years"],
        silent=True
    )
    
    # ============================================================
    # SECTION 10: EMERGENCY MEDICINE - Drs. Shahul & Hisham (8 tests)
    # ============================================================
    print("\n🚨 SECTION 10: EMERGENCY Cases\n")
    
    await test_conversation(
        "EMERG-1: Road accident",
        ["met with accident", "bleeding from head", "severe pain"],
        silent=True
    )
    
    await test_conversation(
        "EMERG-2: Stroke symptoms",
        ["sudden weakness on left side", "can't speak properly", "face drooping"],
        silent=True
    )
    
    await test_conversation(
        "EMERG-3: Seizure",
        ["had a seizure", "unconscious for few minutes", "confused now"],
        silent=True
    )
    
    await test_conversation(
        "EMERG-4: Poisoning",
        ["accidentally drank something toxic", "vomiting", "stomach pain"],
        silent=True
    )
    
    await test_conversation(
        "EMERG-5: Severe trauma",
        ["fell from height", "can't move legs", "severe back pain"],
        silent=True
    )
    
    await test_conversation(
        "EMERG-6: Chest pain crushing",
        ["crushing chest pain", "left arm numb", "sweating heavily"],
        silent=True
    )
    
    await test_conversation(
        "EMERG-7: Severe injury",
        ["deep cut on leg", "bleeding won't stop", "accident"],
        silent=True
    )
    
    await test_conversation(
        "EMERG-8: Breathing stopped",
        ["patient not breathing properly", "resuscitation needed", "urgent"],
        silent=True
    )
    
    # ============================================================
    # SECTION 11: NEUROLOGY - Dr. Shafeeq Usman (7 tests)
    # ============================================================
    print("\n🧠 SECTION 11: NEUROLOGY Cases\n")
    
    await test_conversation(
        "NEURO-1: Severe headache",
        ["worst headache of my life", "sudden onset", "vomiting"],
        silent=True
    )
    
    await test_conversation(
        "NEURO-2: Epilepsy concern",
        ["repeated seizures", "lose consciousness", "family history"],
        silent=True
    )
    
    await test_conversation(
        "NEURO-3: Numbness and tingling",
        ["numbness in hands and feet", "for months", "getting worse"],
        silent=True
    )
    
    await test_conversation(
        "NEURO-4: Parkinson symptoms",
        ["tremors in hands", "difficulty walking", "65 years old"],
        silent=True
    )
    
    await test_conversation(
        "NEURO-5: Weakness one side",
        ["left side of body feels weak", "started yesterday"],
        silent=True
    )
    
    await test_conversation(
        "NEURO-6: Chronic headaches",
        ["headaches every day", "for months", "affecting work"],
        silent=True
    )
    
    await test_conversation(
        "NEURO-7: Memory problems",
        ["forgetting things", "confusion", "70 years old"],
        silent=True
    )
    
    # ============================================================
    # SECTION 12: ONCOLOGY - Drs. Favaz & Tony (6 tests)
    # ============================================================
    print("\n🎗️ SECTION 12: ONCOLOGY Cases\n")
    
    await test_conversation(
        "ONCO-1: Lump detected",
        ["found a lump in breast", "worried about cancer"],
        silent=True
    )
    
    await test_conversation(
        "ONCO-2: Chemotherapy side effects",
        ["on chemotherapy", "severe nausea and weakness"],
        silent=True
    )
    
    await test_conversation(
        "ONCO-3: Cancer diagnosis follow-up",
        ["diagnosed with cancer", "need treatment plan"],
        silent=True
    )
    
    await test_conversation(
        "ONCO-4: Ovarian cancer symptoms",
        ["abdominal bloating", "pelvic pain", "weight loss"],
        silent=True
    )
    
    await test_conversation(
        "ONCO-5: Tumor pain management",
        ["severe pain from tumor", "need pain relief"],
        silent=True
    )
    
    await test_conversation(
        "ONCO-6: Biopsy required",
        ["doctor said I need biopsy", "suspicious mass found"],
        silent=True
    )
    
    # ============================================================
    # SECTION 13: OPHTHALMOLOGY - Dr. Bindiya (6 tests)
    # ============================================================
    print("\n👁️ SECTION 13: OPHTHALMOLOGY Cases\n")
    
    await test_conversation(
        "OPTHAL-1: Blurred vision",
        ["vision is blurry", "for 2 weeks", "difficulty reading"],
        silent=True
    )
    
    await test_conversation(
        "OPTHAL-2: Red painful eye",
        ["red eye with pain", "light sensitive", "discharge"],
        silent=True
    )
    
    await test_conversation(
        "OPTHAL-3: Cataract suspected",
        ["cloudy vision", "70 years old", "progressive"],
        silent=True
    )
    
    await test_conversation(
        "OPTHAL-4: Diabetic eye check",
        ["I'm diabetic", "need eye checkup", "vision slightly affected"],
        silent=True
    )
    
    await test_conversation(
        "OPTHAL-5: Dry eyes",
        ["eyes always dry and irritated", "burning sensation"],
        silent=True
    )
    
    await test_conversation(
        "OPTHAL-6: Glaucoma concern",
        ["eye pressure high", "peripheral vision loss", "family history"],
        silent=True
    )
    
    # ============================================================
    # SECTION 14: MIXED COMPLEX SCENARIOS (10 tests)
    # ============================================================
    print("\n🔀 SECTION 14: COMPLEX MIXED Cases\n")
    
    await test_conversation(
        "COMPLEX-1: Multiple symptoms unclear",
        ["fever, cough, chest pain, diarrhea", "for 3 days", "very confused"],
        silent=True
    )
    
    await test_conversation(
        "COMPLEX-2: Diabetic with multiple issues",
        ["I'm diabetic, now have foot pain and blurred vision"],
        silent=True
    )
    
    await test_conversation(
        "COMPLEX-3: Elderly multiple complaints",
        ["I'm 75, have joint pain, breathlessness, and confusion"],
        silent=True
    )
    
    await test_conversation(
        "COMPLEX-4: Pregnancy with complications",
        ["pregnant, severe headache, blurred vision, swelling"],
        silent=True
    )
    
    await test_conversation(
        "COMPLEX-5: Post-surgery complications",
        ["had surgery 2 weeks ago, wound not healing, fever"],
        silent=True
    )
    
    await test_conversation(
        "COMPLEX-6: Chronic pain multiple sites",
        ["pain everywhere - head, stomach, joints", "for months"],
        silent=True
    )
    
    await test_conversation(
        "COMPLEX-7: Mental health with physical symptoms",
        ["can't sleep, anxiety, chest pain, palpitations"],
        silent=True
    )
    
    await test_conversation(
        "COMPLEX-8: Medication side effects",
        ["on multiple medications, now dizzy and nauseous"],
        silent=True
    )
    
    await test_conversation(
        "COMPLEX-9: Travel-related illness",
        ["came back from trip, high fever, rash, diarrhea"],
        silent=True
    )
    
    await test_conversation(
        "COMPLEX-10: Autoimmune suspected",
        ["joint pain, rash, fatigue, hair loss", "for months"],
        silent=True
    )
    
    print("\n" + "="*100)
    print("✅ ALL 100+ TESTS COMPLETED - Generating Summary...")
    print("="*100 + "\n")
    
    # Print results
    results.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
