import os
import unittest
import json
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup test environment before imports
os.environ["OPENAI_API_KEY"] = ""  # Force fallback rule-based mode for predictable testing

from database import Base, Lead, ChatSession, get_db
from main import app
from qualification_engine import (
    verify_service_area,
    heuristic_classify_service,
    heuristic_classify_urgency,
    heuristic_classify_budget,
    calculate_lead_score,
    get_lead_category
)
from conversation_agent import check_immediate_escalation, run_rule_based_fallback, process_chat_message

# Setup isolated test database
TEST_DB_PATH = "/home/team/shared/ai-engine/test_hvac_leads.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply db dependency override in FastAPI app
app.dependency_overrides[get_db] = override_get_db

class TestHVACAIEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create test tables
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Drop test tables and clean up DB file
        Base.metadata.drop_all(bind=engine)
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def setUp(self):
        # Clear database rows before each test
        db = TestingSessionLocal()
        db.query(ChatSession).delete()
        db.query(Lead).delete()
        db.commit()
        db.close()

    # --- 1. Unit Tests: Qualification Engine ---

    def test_service_classification(self):
        self.assertEqual(heuristic_classify_service("My AC is blowing warm air"), "AC Repair")
        self.assertEqual(heuristic_classify_service("Need a quote on a new air conditioner"), "AC Installation")
        self.assertEqual(heuristic_classify_service("Our furnace won't turn on, freezing"), "Furnace Repair")
        self.assertEqual(heuristic_classify_service("Heater replacement estimate"), "Furnace Installation")
        self.assertEqual(heuristic_classify_service("There is a massive gas leak in the basement"), "Emergency")
        self.assertEqual(heuristic_classify_service("Want to schedule a spring tune up"), "Maintenance")

    def test_urgency_classification(self):
        self.assertEqual(heuristic_classify_urgency("it is freezing, heater is dead", "Furnace Repair"), "Hot")
        self.assertEqual(heuristic_classify_urgency("pricing inquiry for next month replacement", "AC Installation"), "Warm")
        self.assertEqual(heuristic_classify_urgency("just researching typical heat pump costs", "Heat Pump"), "Cold")

    def test_service_area_verification(self):
        # Austin TX core zip
        res_core = verify_service_area("78701")
        self.assertTrue(res_core["is_served"])
        self.assertEqual(res_core["tier"], "core")
        self.assertEqual(res_core["city"], "Austin")

        # Round Rock TX nearby zip
        res_nearby = verify_service_area("78664")
        self.assertTrue(res_nearby["is_served"])
        self.assertEqual(res_nearby["tier"], "nearby")

        # Unsupported zip
        res_unsupported = verify_service_area("90210")
        self.assertFalse(res_unsupported["is_served"])
        self.assertEqual(res_unsupported["tier"], "unsupported")

        # Invalid zip
        res_invalid = verify_service_area("not-a-zip")
        self.assertFalse(res_invalid["is_served"])
        self.assertEqual(res_invalid["tier"], "invalid")

    def test_lead_scoring_logic(self):
        # Hot emergency lead, served core area, with contact details and booked
        score_hot = calculate_lead_score(
            service_classification="Emergency",
            urgency="Hot",
            budget_status="Ready to buy",
            zip_code="78701",
            has_contact_info=True,
            appointment_ready=True,
            appointment_booked=True
        )
        # Components: Emergency (20) + Hot (30) + Ready (20) + Core Served (20) + Contact & Booked (10) = 100
        self.assertEqual(score_hot, 100)
        self.assertEqual(get_lead_category(score_hot), "Hot")

        # Warm maintenance lead, nearby area, has contact, not booked
        score_warm = calculate_lead_score(
            service_classification="Maintenance",
            urgency="Warm",
            budget_status="Comparing",
            zip_code="78664",
            has_contact_info=True,
            appointment_ready=False,
            appointment_booked=False
        )
        # Components: Maintenance (10) + Warm (15) + Comparing (10) + Nearby Served (15) + Contact (5) = 55
        self.assertEqual(score_warm, 55)
        self.assertEqual(get_lead_category(score_warm), "Warm")

        # Out of area lead, researching
        score_cold = calculate_lead_score(
            service_classification="IAQ",
            urgency="Cold",
            budget_status="Unknown",
            zip_code="90210",
            has_contact_info=False,
            appointment_ready=False,
            appointment_booked=False
        )
        # Components: IAQ (10) + Cold (5) + Unknown (5) + Out of area (0) + Contact (0) = 20
        self.assertEqual(score_cold, 20)
        self.assertEqual(get_lead_category(score_cold), "Cold")

    # --- 2. Unit Tests: Conversational Escalations ---

    def test_escalation_checks(self):
        # Emergency
        esc, reason = check_immediate_escalation("Help, I smell a gas leak in my kitchen!")
        self.assertTrue(esc)
        self.assertIn("gas leak", reason)

        # Human requested
        esc, reason = check_immediate_escalation("Can I speak to a human representative please?")
        self.assertTrue(esc)
        self.assertIn("human", reason)

        # Frustration
        esc, reason = check_immediate_escalation("This is a stupid bot, waste of time")
        self.assertTrue(esc)
        self.assertIn("frustration", reason)

        # Standard conversational text - no escalation
        esc, reason = check_immediate_escalation("My AC is broken, I would like to schedule a repair.")
        self.assertFalse(esc)
        self.assertIsNone(reason)

    # --- 3. Integration Tests: Chat processing and Session States ---

    def test_rule_based_fallback_workflow(self):
        session_id = str(uuid.uuid4())
        db = TestingSessionLocal()

        # Step 1: Send Greeting / Ask Name
        res1 = process_chat_message(db, session_id, "Hello")
        self.assertEqual(res1["current_step"], "ask_name")
        self.assertIn("name", res1["response_message"])

        # Step 2: Provide Name / Ask ZIP
        res2 = process_chat_message(db, session_id, "My name is John Doe")
        self.assertEqual(res2["current_step"], "ask_zip")
        self.assertEqual(res2["lead"].first_name, "John")
        self.assertEqual(res2["lead"].last_name, "Doe")

        # Step 3: Provide ZIP / Ask Service
        res3 = process_chat_message(db, session_id, "78701")
        self.assertEqual(res3["current_step"], "ask_service")
        self.assertEqual(res3["lead"].zip_code, "78701")
        self.assertEqual(res3["lead"].city, "Austin")

        # Step 4: Describe Issue / Ask Contact info
        res4 = process_chat_message(db, session_id, "My central AC is blowing hot warm air, need repair")
        self.assertEqual(res4["current_step"], "ask_contact")
        self.assertEqual(res4["lead"].service_classification, "AC Repair")
        self.assertEqual(res4["lead"].urgency, "Hot")

        # Step 5: Provide Contact details / Ask Booking options
        res5 = process_chat_message(db, session_id, "Call me at 512-555-0199 or email john@example.com")
        self.assertEqual(res5["current_step"], "book_appointment")
        self.assertEqual(res5["lead"].phone, "512-555-0199")
        self.assertEqual(res5["lead"].email, "john@example.com")

        # Step 6: Select arrival slot / Book Appointment (Comfort Club accepted)
        res6 = process_chat_message(db, session_id, "I would like option 1 today and yes please add the comfort club")
        self.assertEqual(res6["current_step"], "completed")
        self.assertTrue(res6["lead"].appointment_booked)
        self.assertEqual(res6["lead"].status, "booked")
        self.assertGreaterEqual(res6["lead"].lead_score, 80)

        db.close()

    # --- 4. API Layer Endpoints (FastAPI TestClient) ---

    def test_api_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_api_qualify(self):
        payload = {
            "zip_code": "78704",
            "service_needed": "My heater is broken and leaking. I am ready to buy a new system today.",
            "phone": "512-555-1234",
            "email": "test@example.com"
        }
        response = self.client.post("/api/qualify", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_served"])
        self.assertEqual(data["city"], "Austin")
        self.assertEqual(data["service_classification"], "Furnace Repair") # Heuristic fallback
        self.assertEqual(data["urgency"], "Hot")
        self.assertEqual(data["budget_status"], "Ready to buy")
        self.assertGreater(data["lead_score"], 70)

    def test_api_chat_and_leads_crud(self):
        # 1. Create a lead via chat message
        session_id = str(uuid.uuid4())
        payload = {
            "session_id": session_id,
            "message": "Hi, I am Bob Jones"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        chat_data = response.json()
        self.assertEqual(chat_data["current_step"], "ask_zip")
        self.assertEqual(chat_data["lead"]["first_name"], "Bob")
        self.assertEqual(chat_data["lead"]["last_name"], "Jones")
        lead_id = chat_data["lead"]["id"]

        # 2. Query all leads via GET /api/leads
        response_leads = self.client.get("/api/leads")
        self.assertEqual(response_leads.status_code, 200)
        leads_list = response_leads.json()
        self.assertGreaterEqual(len(leads_list), 1)
        self.assertTrue(any(l["id"] == lead_id for l in leads_list))

        # 3. Retrieve single lead details
        response_single = self.client.get(f"/api/leads/{lead_id}")
        self.assertEqual(response_single.status_code, 200)
        self.assertEqual(response_single.json()["first_name"], "Bob")

        # 4. Delete the lead
        response_delete = self.client.delete(f"/api/leads/{lead_id}")
        self.assertEqual(response_delete.status_code, 200)
        self.assertTrue(response_delete.json()["success"])

        # 5. Verify 404 on deleted lead
        response_check_404 = self.client.get(f"/api/leads/{lead_id}")
        self.assertEqual(response_check_404.status_code, 404)

if __name__ == "__main__":
    unittest.main()
