import os
import datetime
import uuid
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_PATH = "/home/team/shared/ai-engine/hvac_leads.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    service_needed = Column(Text, nullable=True)  # Raw user description
    service_classification = Column(String, nullable=True)  # AC Repair, etc.
    urgency = Column(String, nullable=True)  # Hot, Warm, Cold
    budget_status = Column(String, nullable=True)  # Ready to buy, Needs financing, Comparing, Unknown
    lead_score = Column(Integer, default=0)
    lead_score_category = Column(String, nullable=True)  # Hot, Warm, Cold
    appointment_readiness = Column(Boolean, default=False)
    appointment_booked = Column(Boolean, default=False)
    status = Column(String, default="new")  # new, qualified, booked, escalated, nurturing
    escalated = Column(Boolean, default=False)
    escalation_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    sessions = relationship("ChatSession", back_populates="lead")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    session_id = Column(String, primary_key=True)
    lead_id = Column(String, ForeignKey("leads.id"), nullable=True)
    messages = Column(Text, default="[]")  # JSON serialized list of dicts
    current_step = Column(String, default="greeting")  # greeting, ask_name, ask_contact, ask_zip, ask_service, book_appointment, completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    lead = relationship("Lead", back_populates="sessions")

# Initialize SQLite database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Create parent directory if needed
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
