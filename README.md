# HVAC AI Employee — Core Conversation & Lead Qualification Engine

This repository contains the core "brain" of the **HVAC AI Employee** platform—a modular, stateful Python backend built with **FastAPI**, **SQLAlchemy**, and **OpenAI GPT-4o-mini** (featuring an intelligent rule-based fallback). It is designed to capture, qualify, score, and book HVAC leads 24/7 in under 5 seconds.

---

## 🚀 Business Value & Promises

- **Never Miss a Lead:** Speed-to-lead response under 5 seconds, capturing website, SMS, and chat leads instantly.
- **Autonomous Lead Qualification:** Automated evaluation of customer needs, service areas, budget readiness, and urgency.
- **Autonomous Appointment Booking:** Intelligently maps customer availability and guides them into booking slots while upselling maintenance membership plans.
- **Zero-Downtime Reliability:** Implements a deterministic **Rule-Based Fallback** state-machine that ensures continuous lead intake and booking functionality even if downstream LLM APIs suffer outages.
- **Safety First:** Immediate human escalation for safety hazards (gas leaks, smoke, sparks, carbon monoxide) and explicit customer assistance requests.

---

## 🛠️ Key Architectural Modules

### 1. Lead Qualification Engine (`qualification_engine.py`)
Classifies service requests and evaluates the potential of every inbound lead:
- **Service Classification:** Categorizes the exact service needed: `AC Repair`, `AC Installation`, `Furnace Repair`, `Furnace Installation`, `Heat Pump`, `IAQ`, `Maintenance`, or `Emergency`.
- **Urgency Scoring:**
  - **Hot:** No cooling/heating in extreme temperatures, water leaks, or safety hazards.
  - **Warm:** Standard scheduling, replacement planning, quote comparisons.
  - **Cold:** General research, long-term future planning.
- **Service Area Verification:** Verifies 5-digit ZIP codes against core service regions (Austin, TX) and extended dispatch areas (Round Rock, Pflugerville, Cedar Park, TX).
- **Budget Qualification:** Determines purchase intent: `Ready to buy`, `Needs financing`, `Comparing`, or `Unknown`.

### 2. Lead Scoring System (`qualification_engine.py`)
Computes a dynamic **0–100 score** based on:
- Service type and intent (up to 20 pts)
- Urgency level (up to 30 pts)
- Budget readiness (up to 20 pts)
- Location verification (up to 20 pts)
- Contact details provided & appointment readiness (up to 10 pts)

**Follow-Up Categorization:**
- **Hot (80–100):** Book immediately.
- **Warm (50–79):** Short-term nurture.
- **Cold (0–49):** Long-term database nurture.

### 3. AI Conversation Agent (`conversation_agent.py`)
A stateful conversation manager supporting standard funnel-progression states:
```
[greeting] ➔ [ask_name] ➔ [ask_zip] ➔ [ask_service] ➔ [ask_contact] ➔ [book_appointment] ➔ [completed]
```
- **Dual-Model Processing:** Primarily uses OpenAI GPT-4o-mini with structured JSON parsing to update session states. Automatically activates the deterministic rule-based script fallback on API failure or empty keys.
- **Strict Guardrails:** Never claims to be a technician. Does not give diagnostic advice. Focuses strictly on qualification and appointment scheduling.
- **Red Flag Escalation:** Monitored continuously for emergency terms (gas, smoke, carbon monoxide, sparks, fire) or human requests, which immediately switch the session status to `escalated` and instruct the user to call local emergency dispatch or prompt manual staff takeover.

---

## 🗄️ Database Schema & Models (`database.py`)

A persistent database layer using SQLAlchemy and SQLite:
- **`leads` Table:** Stores full structured customer details including contact info (`phone`, `email`), classification, urgency, budget status, calculated `lead_score`, appointment booking status, and human escalation flags.
- **`chat_sessions` Table:** Maintains stateful message history logs as serialized JSON lists and keeps track of the customer's `current_step` in the booking pipeline.

---

## 🔌 API Reference (`main.py`)

The backend exposes a clean HTTP REST interface:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/health` | `GET` | Simple health-check indicating system, API, and database status. |
| `/api/chat` | `POST` | Stateful conversational chat processing. Accepts a `session_id` and raw user `message`. Returns the updated conversation state and lead details. |
| `/api/qualify` | `POST` | Stateless, real-time qualification tool that instantly processes ZIP code, service description, and contact presence. Useful for quick external form parsing. |
| `/api/leads` | `GET` | Retrieves a chronological list of all captured leads. |
| `/api/leads/{id}` | `GET` | Retrieves detailed parameters for a single lead. |
| `/api/leads/{id}` | `DELETE` | Removes a lead and its associated chat session histories from the database. |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- `pip` package manager

### 1. Clone & Set Up Directory
```bash
git clone https://github.com/snehasish23/Havac-lead-.git
cd Havac-lead-
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create your environment variables:
```bash
export OPENAI_API_KEY="your-api-key-here"
export PORT=3000
```
*Note: If `OPENAI_API_KEY` is omitted, the engine will automatically run in rule-based fallback mode.*

### 5. Start the Server
```bash
python main.py
```
The FastAPI documentation will be available at `http://localhost:3000/docs` (Swagger UI) and `http://localhost:3000/redoc`.

---

## 🧪 Testing

The repository contains a comprehensive suite of unit and integration tests covering qualification heuristics, scoring logic, escalation checks, fallback behavior, and full API endpoint simulation (via FastAPI TestClient).

To execute the test suite:
```bash
python -m unittest test_ai_engine.py
```
