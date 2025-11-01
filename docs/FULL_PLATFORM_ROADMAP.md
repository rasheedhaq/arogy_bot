# Full-Fledged Medical Platform - Implementation Plan

## End-to-End Flow

```
[User Message] 
    ↓
[8-Question Medical History]
    ↓
[AI Symptom Analysis]
    ↓
[Phase 1: Doctor Matching] ← Current MVP
    ↓
[Phase 2: Availability Check] ← Next
    ↓
[Phase 3: Location Filtering] ← Next
    ↓
[Phase 4: Booking System] ← Next
    ↓
[Phase 5: Payment Gateway] ← Future
    ↓
[Phase 6: Follow-up & Reviews] ← Future
```

---

## Phase 1: Doctor Matching (Current MVP)

### Database Required
- ✅ Doctor info (name, specialty, qualification)
- ✅ Symptom mapping (primary, secondary, exclude keywords)
- ✅ Basic contact (phone, email)
- ✅ Location (address, pincode)

### Algorithm
1. LLM identifies specialty and symptoms from user input
2. Search doctors by:
   - Exact specialty match
   - Primary symptom match (weight: 10)
   - Secondary symptom match (weight: 5)
   - Exclude keyword negative match (weight: -100)
3. Return top 2 doctors

### Issue to Fix
- ❌ Current: Generic keywords → Oncologist matches tooth pain
- ✅ Fixed: Explicit exclude_keywords field prevents mismatch

---

## Phase 2: Availability & Booking

### Database Fields Needed
```csv
consultation_days,consultation_hours_start,consultation_hours_end,
online_consult_available,appointment_required,average_wait_time_mins,
slots_available_today
```

### New Flow
```
Select Doctor 
    ↓
Check Availability
    ├─ Today: 3 slots available
    ├─ Tomorrow: 5 slots available
    ├─ Online: Available 2-6 PM
    └─ In-person: Available 10 AM-12 PM
    ↓
Choose Time Slot
    ↓
Confirm Booking
```

### Data Source
- **Static:** consultation_days, hours, online option (CSV)
- **Real-time:** slots_available_today (from booking API)

### Technology
- Calendar integration (React Calendar / FullCalendar)
- Real-time slot API (can integrate with:
  - Practo API
  - Docktor API
  - Custom booking table)

---

## Phase 3: Location-Based Filtering

### Database Fields Needed
```csv
latitude,longitude,city,pincode,google_maps_link
```

### New Flow
```
Doctor List + Location
    ↓
Show distance from user
    ├─ 2.5 km away
    ├─ 5.1 km away
    └─ 8.3 km away
    ↓
Filter by distance (3km, 5km, 10km)
    ↓
Show on map
```

### Technology
- Google Maps API (distance matrix)
- Geolocation (user's current location)
- Distance calculation

### Integration Points
```
User pincode: 670331
↓
Find doctors in same area first
↓
Show distance to each
↓
Sort by proximity
```

---

## Phase 4: Booking & Appointment

### New Database Tables

#### BOOKINGS Table
```
booking_id (UUID)
user_id
doctor_id
appointment_date (YYYY-MM-DD)
appointment_time (HH:MM)
consultation_type (in-person | online)
status (confirmed | cancelled | completed)
created_at
```

#### USERS Table
```
user_id (UUID)
phone_number (unique)
full_name
age
gender
email
home_address
pincode
created_at
```

### New Flow
```
Select Time Slot
    ↓
Enter Patient Details (if not registered)
    ├─ Name
    ├─ Age
    ├─ Gender
    ├─ Contact
    └─ Address
    ↓
Confirm Appointment
    ↓
Send Confirmation (SMS + Notification)
    ↓
Option to Pay Now (Phase 5)
```

### Features
- SMS confirmation (Twillio / AWS SNS)
- Reminder 24 hours before
- Cancellation option
- Doctor dashboard to see bookings

---

## Phase 5: Payment Gateway Integration

### Database Fields Needed
```csv
consultation_fee,
online_fee,
home_visit_fee,
insurance_accepted,
payment_gateway_id
```

### New Database Tables

#### PAYMENTS Table
```
payment_id (UUID)
booking_id (FK)
amount
currency (INR)
payment_method (card | upi | netbanking)
payment_status (pending | success | failed)
transaction_id
razorpay_order_id
created_at
```

### Payment Providers (Research)

#### **Razorpay** (Recommended for India)
- ✅ Easy integration
- ✅ UPI + Card + Net Banking
- ✅ Settlement in 2 days
- ✅ No hidden charges
- Link: https://razorpay.com

#### **PayU**
- ✅ Popular in India
- ✅ Supports installments
- Link: https://payu.in

#### **Stripe** (International)
- ✅ Global coverage
- ❌ Higher fees for India
- Link: https://stripe.com

#### **PhonePe Business** (UPI)
- ✅ UPI only (simple)
- ✅ Low commission
- Link: https://business.phonepe.com

### New Flow
```
Appointment Confirmed
    ↓
Optional: Pay Now
    ├─ Razorpay Modal
    ├─ Choose payment method (UPI/Card/NetBanking)
    └─ Process payment
    ↓
Payment Success / Failure
    ↓
Confirmation with receipt
```

### Implementation
```python
# Example integration
def process_payment(booking_id, amount):
    # Create Razorpay order
    order = client.order.create(
        amount=amount*100,  # In paise
        currency="INR",
        notes={"booking_id": booking_id}
    )
    
    # Store in database
    Payment.create(
        booking_id=booking_id,
        razorpay_order_id=order['id'],
        amount=amount
    )
    
    # Return to frontend for modal
    return order
```

---

## Phase 6: Follow-up & Reviews

### Database Tables

#### REVIEWS Table
```
review_id
booking_id (FK)
doctor_id (FK)
user_id (FK)
rating (1-5)
comment (text)
created_at
```

#### FOLLOW_UPS Table
```
followup_id
booking_id (FK)
scheduled_date
reminder_sent (bool)
```

### Features
- Rating after appointment (1-5 stars)
- Text review option
- Follow-up appointment suggestion
- Review display on doctor profile

---

# Implementation Timeline

## MVP (Now - Week 1)
- ✅ Symptoms → Doctor list
- ✅ Fix specialty matching (exclude_keywords)
- ✅ Basic contact info

## Phase 2 (Week 2-3)
- ⏳ Add availability fields to CSV
- ⏳ Booking UI (date/time picker)
- ⏳ Simple slot system

## Phase 3 (Week 4)
- ⏳ Location field mapping
- ⏳ Distance calculation
- ⏳ Google Maps integration

## Phase 4 (Week 5-6)
- ⏳ User registration
- ⏳ Booking confirmation
- ⏳ SMS notifications

## Phase 5 (Week 7-8)
- ⏳ Razorpay integration
- ⏳ Payment processing
- ⏳ Invoice generation

## Phase 6 (Week 9-10)
- ⏳ Reviews system
- ⏳ Follow-up tracking
- ⏳ Analytics dashboard

---

# Data Sources & APIs

## Booking System Options

| Platform | Cost | Integration | Data |
|----------|------|-----------|------|
| **Practo** | Contact | API | 50,000+ doctors |
| **Docktor** | Varies | API | Regional doctors |
| **Zocdoc** | Free | API | Global |
| **Custom DB** | Low | CSV Upload | Your doctors |

## Payment Gateways

| Provider | Setup Fee | Transaction Fee | Settlement |
|----------|-----------|-----------------|-----------|
| **Razorpay** | ₹0 | 2% + ₹3 | 2 days |
| **PayU** | ₹0 | 1.5-2% | 1-2 days |
| **Stripe** | ₹0 | 2.9% + $0.30 | 2-3 days |

## SMS Providers

| Provider | Cost/SMS | Integration | Volume Discount |
|----------|----------|-------------|-----------------|
| **Twillio** | ₹1.5 | Easy | Yes @ 1000+ |
| **AWS SNS** | ₹0.50 | Easy | Volume based |
| **Exotel** | ₹1 | Easy | Yes |

---

# Test Scenarios

## Test Case 1: Tooth Pain (The Bug)
```
Input: "tooth pain"
Expected: Dentist (Dr. Priya)
Actual Before: Oncologist (WRONG)
Actual After: Dentist (CORRECT)
```

## Test Case 2: Chest Pain (Critical)
```
Input: "chest pain"
Expected: Cardiologist (Dr. Rajesh)
Status: ✅ Correct
```

## Test Case 3: Stomach Pain
```
Input: "stomach pain"
Expected: Gastroenterologist (Dr. Neha)
Status: Need to verify
```

---

# Questions for Your Team

## For Data Entry Person
1. Can you collect doctor details matching DATA_SCHEMA.md?
2. Do you have specialty-symptom mappings validated by doctors?
3. Can you update CSV weekly with new doctors?

## For Tech Team
1. Which payment gateway to integrate? (Razorpay recommended)
2. Can you set up Twillio for SMS?
3. Do you have Google Maps API key?
4. Can you build booking calendar UI?

## For Business
1. Commission model: % per booking or flat fee?
2. Insurance integration: Which insurances to support?
3. Marketing: How to get first 100 doctors?
4. Support: Who handles customer queries?

