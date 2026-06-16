import os
import uuid
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import init_db, get_db, Lead, ChatSession
from qualification_engine import verify_service_area, calculate_lead_score, get_lead_category
from conversation_agent import process_chat_message

# Initialize database tables
init_db()

app = FastAPI(
    title="HVAC AI Employee - Core API",
    description="The intelligent backend powering Lead Qualification & Autonomous AI Conversational Agents.",
    version="1.0.0"
)

# Enable CORS for local testing and full-stack integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Schema Models ---

class ChatRequest(BaseModel):
    session_id: str = Field(default_name="session_id", description="Session UUID for message thread")
    message: str = Field(..., description="The user's text message")

class LeadResponse(BaseModel):
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    service_classification: Optional[str] = None
    urgency: Optional[str] = None
    budget_status: Optional[str] = None
    lead_score: int
    lead_score_category: Optional[str] = None
    appointment_booked: bool
    status: str
    escalated: bool
    escalation_reason: Optional[str] = None

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    response_message: str
    session_id: str
    current_step: str
    escalated: bool
    escalation_reason: Optional[str] = None
    lead: LeadResponse

class QualifyRequest(BaseModel):
    zip_code: Optional[str] = None
    service_needed: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class QualifyResponse(BaseModel):
    is_served: bool
    city: Optional[str] = None
    state: Optional[str] = None
    tier: str
    distance_miles: Optional[int] = None
    service_classification: str
    urgency: str
    budget_status: str
    lead_score: int
    lead_score_category: str
    message: str

# --- API Route Handlers ---

@app.get("/api/health")
def health_check():
    """Simple health monitoring endpoint."""
    return {"status": "healthy", "engine": "Python/FastAPI", "db": "SQLite"}

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Core conversational endpoint.
    Processes the message, executes LLM extraction/fallback logic, qualifies, 
    persists results to SQLite, and returns agent response + updated lead details.
    """
    try:
        result = process_chat_message(db, payload.session_id, payload.message)
        return result
    except Exception as e:
        import traceback
        print("Error processing chat message:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")

@app.post("/api/qualify", response_model=QualifyResponse)
def qualify_endpoint(payload: QualifyRequest):
    """
    Direct Lead Qualification Engine API.
    Runs location verification, classification heuristic and score computation instantly.
    """
    # 1. Location check
    loc_info = verify_service_area(payload.zip_code)
    
    # 2. Heuristics for service/urgency/budget classification
    from qualification_engine import (
        heuristic_classify_service,
        heuristic_classify_urgency,
        heuristic_classify_budget
    )
    
    service_needed_text = payload.service_needed or ""
    classification = heuristic_classify_service(service_needed_text)
    urgency = heuristic_classify_urgency(service_needed_text, classification)
    budget = heuristic_classify_budget(service_needed_text)
    
    # 3. Lead score
    has_contact = bool(payload.phone or payload.email)
    score = calculate_lead_score(
        service_classification=classification,
        urgency=urgency,
        budget_status=budget,
        zip_code=payload.zip_code,
        has_contact_info=has_contact,
        appointment_ready=False,
        appointment_booked=False
    )
    category = get_lead_category(score)
    
    return {
        "is_served": loc_info["is_served"],
        "city": loc_info["city"],
        "state": loc_info["state"],
        "tier": loc_info["tier"],
        "distance_miles": loc_info["distance_miles"],
        "service_classification": classification,
        "urgency": urgency,
        "budget_status": budget,
        "lead_score": score,
        "lead_score_category": category,
        "message": loc_info["message"]
    }

@app.get("/api/leads", response_model=List[LeadResponse])
def get_leads_endpoint(db: Session = Depends(get_db)):
    """Retrieves all qualified and incoming leads stored in the database."""
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
    return leads

@app.get("/api/leads/{lead_id}", response_model=LeadResponse)
def get_lead_by_id_endpoint(lead_id: str, db: Session = Depends(get_db)):
    """Gets details for a single lead."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@app.delete("/api/leads/{lead_id}")
def delete_lead_endpoint(lead_id: str, db: Session = Depends(get_db)):
    """Deletes a lead and its associated chat sessions from the database."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Remove sessions first
    db.query(ChatSession).filter(ChatSession.lead_id == lead_id).delete()
    db.delete(lead)
    db.commit()
    return {"success": True, "message": f"Lead {lead_id} successfully deleted."}

# --- Serve Shared Frontend if Available ---
# This serves static files built by the Product Engineer seamlessly from /home/team/shared/website/dist or /home/team/shared/website/
dist_path = "/home/team/shared/website/dist"
static_path = "/home/team/shared/website"

if os.path.exists(dist_path) and os.listdir(dist_path):
    print(f"Mounting built static frontend from {dist_path}")
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")
elif os.path.exists(static_path) and any(f.endswith(".html") for f in os.listdir(static_path)):
    print(f"Mounting dev static frontend from {static_path}")
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")
else:
    # Basic landing page greeting if website is completely empty
    @app.get("/")
    def root_greeting():
        return {
            "name": "HVAC AI Employee - Conversation Agent Backend",
            "status": "Online and Listening on Port 3000",
            "api_docs": "/docs",
            "message": "Welcome! Please check our API endpoints or connect your front-end user interface."
        }

if __name__ == "__main__":
    import uvicorn
    # Bind to all interfaces (0.0.0.0) on port 3000 as required
    port = int(os.environ.get("PORT", 3000))
    print(f"Starting HVAC AI Employee Core API on port {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
