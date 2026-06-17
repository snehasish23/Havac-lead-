import os
import json
import re
from typing import Dict, Any, List, Tuple, Optional
from sqlalchemy.orm import Session
import openai

from database import Lead, ChatSession
from qualification_engine import (
    heuristic_classify_service,
    heuristic_classify_urgency,
    heuristic_classify_budget,
    calculate_lead_score,
    get_lead_category,
    verify_service_area
)

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DEFAULT_MODEL = os.environ.get("OPENAI_MODEL_NAME", "gpt-4o-mini")

# Heuristics for direct human escalation detection
EMERGENCY_WORDS = ["gas leak", "carbon monoxide", "co leak", "smoke", "sparks", "electrical spark", "fire", "burning smell"]
HUMAN_REQUEST_WORDS = ["speak to human", "real person", "agent", "representative", "human", "talk to someone", "operator", "human support", "bypass bot"]
FRUSTRATION_WORDS = ["terrible", "awful", "stupid bot", "hate", "frustrated", "useless", "scam", "waste of time"]

def check_immediate_escalation(text: str) -> Tuple[bool, Optional[str]]:
    """
    Checks if raw text contains immediate human escalation triggers.
    Returns (should_escalate, reason)
    """
    text_lower = text.lower()
    
    # 1. Emergencies
    for word in EMERGENCY_WORDS:
        if word in text_lower:
            return True, f"Emergency safety hazard detected: {word}"
            
    # 2. Human requested
    for word in HUMAN_REQUEST_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", text_lower):
            return True, "User requested human agent escalation."
            
    # 3. Frustration
    for word in FRUSTRATION_WORDS:
        if word in text_lower:
            return True, f"High user frustration detected: '{word}'"
            
    return False, None

def run_rule_based_fallback(
    user_message: str,
    session_history: List[Dict[str, str]],
    current_step: str,
    lead: Optional[Lead] = None
) -> Tuple[str, str, Dict[str, Any]]:
    """
    Highly advanced rule-based conversation engine that acts as an intelligent fallback.
    Maintains flow steps: greeting -> ask_name -> ask_contact -> ask_zip -> ask_service -> book_appointment -> completed
    
    Returns: (response_message, next_step, extracted_info)
    """
    msg_lower = user_message.lower()
    extracted_info = {}
    
    # Pre-extract any obvious info from the message
    # 1. Phone number
    phone_match = re.search(r"\(?\b[2-9][0-9]{2}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b", user_message)
    if phone_match:
        extracted_info["phone"] = phone_match.group(0)
        
    # 2. Email
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", user_message)
    if email_match:
        extracted_info["email"] = email_match.group(0)
        
    # 3. ZIP code
    zip_match = re.search(r"\b\d{5}\b", user_message)
    if zip_match:
        extracted_info["zip_code"] = zip_match.group(0)

    # 4. Name extraction fallback (simple heuristic: "my name is [Name]" or "I'm [Name]")
    name_match = re.search(r"\b(?:my name is|i'm|i am)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", user_message, re.IGNORECASE)
    if name_match:
        name_parts = name_match.group(1).split()
        extracted_info["first_name"] = name_parts[0]
        if len(name_parts) > 1:
            extracted_info["last_name"] = name_parts[1]

    # Service classifications
    service_type = heuristic_classify_service(user_message)
    if service_type and current_step == "ask_service":
        extracted_info["service_classification"] = service_type
        extracted_info["service_needed"] = user_message

    # Transition states and generate response
    if current_step == "greeting":
        first_name = extracted_info.get("first_name")
        if first_name:
            response = f"Nice to meet you, {first_name}! What ZIP code are we looking to service today?"
            return response, "ask_zip", extracted_info
        else:
            response = (
                "Hi! Thanks for contacting HVAC AI Employee, your 24/7 autonomous home comfort assistant. "
                "I can verify your service area, qualify your repair or install needs, and book your technician in seconds!\n\n"
                "To get started, may I please have your name?"
            )
            return response, "ask_name", extracted_info

    elif current_step == "ask_name":
        # Assume the whole message or part of it is the name if not matched by regex
        first_name = extracted_info.get("first_name")
        last_name = extracted_info.get("last_name")
        
        if not first_name:
            # Simple clean up of name input
            clean_name = re.sub(r"^(hi|hello|my name is|i'm|i am|this is)\s+", "", user_message, flags=re.IGNORECASE).strip()
            parts = clean_name.split()
            first_name = parts[0].capitalize() if parts else "Valued Customer"
            last_name = parts[1].capitalize() if len(parts) > 1 else None
            
        extracted_info["first_name"] = first_name
        if last_name:
            extracted_info["last_name"] = last_name
            
        response = f"Nice to meet you, {first_name}! What ZIP code are we looking to service today?"
        return response, "ask_zip", extracted_info

    elif current_step == "ask_zip":
        zip_val = extracted_info.get("zip_code")
        if not zip_val:
            # Take first 5 digit number
            zip_match = re.search(r"\b\d{5}\b", user_message)
            zip_val = zip_match.group(0) if zip_match else None
            
        if not zip_val:
            response = "I wasn't able to catch your 5-digit ZIP code. Could you please provide your ZIP code so I can verify we serve your neighborhood?"
            return response, "ask_zip", extracted_info
            
        extracted_info["zip_code"] = zip_val
        loc_info = verify_service_area(zip_val)
        
        if not loc_info["is_served"]:
            response = (
                f"Thank you. ZIP code {zip_val} is currently outside our immediate HVAC service area. "
                "However, I can escalate your request to our scheduling manager to see if we can accommodate a special trip. "
                "What is the best phone number and email to reach you?"
            )
            return response, "ask_contact", extracted_info
            
        response = f"Great news! We service {loc_info['city']} ({zip_val}) daily.\n\nCould you describe what heating or cooling issues you are experiencing today?"
        return response, "ask_service", extracted_info

    elif current_step == "ask_service":
        # Service classification is already updated from pre-extract
        extracted_info["service_needed"] = user_message
        extracted_info["service_classification"] = service_type
        extracted_info["urgency"] = heuristic_classify_urgency(user_message, service_type)
        extracted_info["budget_status"] = heuristic_classify_budget(user_message)
        
        name = lead.first_name if lead else "there"
        response = (
            f"Got it. It sounds like you need help with {service_type}. "
            f"What is the best phone number and email address to confirm your scheduling options?"
        )
        return response, "ask_contact", extracted_info

    elif current_step == "ask_contact":
        phone = extracted_info.get("phone") or (lead.phone if lead else None)
        email = extracted_info.get("email") or (lead.email if lead else None)
        
        # If not already pre-extracted, try to extract now from message
        if not phone:
            phone_match = re.search(r"\(?\b[2-9][0-9]{2}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b", user_message)
            if phone_match:
                phone = phone_match.group(0)
                extracted_info["phone"] = phone
                
        if not email:
            email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", user_message)
            if email_match:
                email = email_match.group(0)
                extracted_info["email"] = email

        if not phone or not email:
            response = "Thank you! Please make sure to provide both a valid phone number and an email address so we can coordinate your service window."
            return response, "ask_contact", extracted_info
            
        # We have phone and email, now offer booking!
        response = (
            "Perfect, thank you! I have your details on file.\n\n"
            "We have two convenient technician arrival windows open for you:\n"
            "1. Today between 1:00 PM and 5:00 PM\n"
            "2. Tomorrow morning between 8:00 AM and 12:00 PM\n\n"
            "By the way, if you enroll in our Maintenance Comfort Club today for just $19/month, we'll waive today's diagnostic fee and give you a 15% discount on any required repairs! Would you like to select option 1 or 2, and should we add the Comfort Club membership?"
        )
        return response, "book_appointment", extracted_info

    elif current_step == "book_appointment":
        # Check if they booked or mentioned Comfort Club
        comfort_club = any(k in msg_lower for k in ["yes", "comfort club", "membership", "add", "enroll", "sure", "ok", "join"])
        option_booked = None
        
        if "1" in msg_lower or "today" in msg_lower:
            option_booked = "Today 1:00 PM - 5:00 PM"
        elif "2" in msg_lower or "tomorrow" in msg_lower:
            option_booked = "Tomorrow 8:00 AM - 12:00 PM"
            
        if option_booked:
            extracted_info["appointment_booked"] = True
            club_msg = " with your Maintenance Membership pre-enrolled!" if comfort_club else "."
            response = (
                f"Fantastic! I have successfully booked your technician for {option_booked}{club_msg} "
                "A confirmation SMS and calendar invite have been sent to your phone and email. "
                "Thank you for choosing our HVAC services, and have a wonderful day!"
            )
            return response, "completed", extracted_info
        else:
            response = (
                "Which booking window works best for you?\n"
                "1. Today between 1:00 PM and 5:00 PM\n"
                "2. Tomorrow morning between 8:00 AM and 12:00 PM\n\n"
                "Please reply with '1' or '2' to instantly secure your slot."
            )
            return response, "book_appointment", extracted_info

    else:
        # Default fallback completed/unknown state
        response = "I have recorded your booking. Our dispatcher will call you shortly to verify details. Have a great day!"
        return response, "completed", extracted_info

def run_openai_agent(
    user_message: str,
    session_history: List[Dict[str, str]],
    lead: Optional[Lead] = None
) -> Dict[str, Any]:
    """
    State-of-the-art LLM conversation agent with structured JSON output.
    Forces extraction of qualification fields while generating a fluid, professional response.
    """
    openai.api_key = OPENAI_API_KEY
    
    # Format chat history for OpenAI API
    api_messages = [
        {
            "role": "system",
            "content": (
                "You are 'HVAC AI Employee', an autonomous, HVAC-fluent, safety-aware digital booking receptionist.\n"
                "Your objective is to qualify leads, verify service location, book appointments, and offer maintenance memberships to generate maximum revenue.\n\n"
                "CRITICAL INSTRUCTIONS:\n"
                "1. NEVER claim to be a technician. If asked technical troubleshooting questions, explain you are an assistant booking receptionist and will send a certified, licensed technician to diagnose the issue.\n"
                "2. IMMEDIATELY escalate emergencies. If the user mentions a gas leak, carbon monoxide, smoke, active ceiling leaks, or electrical sparks, set 'escalated': true and tell them you are escalating to the emergency dispatch team immediately.\n"
                "3. Follow the AI Decision Framework: greet -> gather name -> gather ZIP code -> gather service description -> gather contact details (phone, email) -> offer appointment arrival windows -> cross-sell Maintenance Comfort Club ($19/mo, waives diagnostic fee, 15% repair discount) -> confirm booking.\n"
                "4. Be professional, friendly, human-like, and direct. Keep responses relatively brief (2-4 sentences max).\n"
                "5. Extract and update the structured lead fields at every turn. If fields are unknown, return null. Preserve existing fields if they were gathered earlier and the user didn't correct them.\n\n"
                "Your output MUST be a valid JSON object matching the following structure:\n"
                "{\n"
                "  \"response_message\": \"The next response to send to the user\",\n"
                "  \"first_name\": \"Extracted first name or null\",\n"
                "  \"last_name\": \"Extracted last name or null\",\n"
                "  \"phone\": \"Extracted phone format like 512-555-0199 or null\",\n"
                "  \"email\": \"Extracted email or null\",\n"
                "  \"zip_code\": \"Extracted 5-digit ZIP code or null\",\n"
                "  \"service_needed\": \"Brief summary of service issues described or null\",\n"
                "  \"service_classification\": \"AC Repair / AC Installation / Furnace Repair / Furnace Installation / Heat Pump / IAQ / Maintenance / Emergency / null\",\n"
                "  \"urgency\": \"Hot / Warm / Cold / null\",\n"
                "  \"budget_status\": \"Ready to buy / Needs financing / Comparing / Unknown / null\",\n"
                "  \"appointment_booked\": true/false,\n"
                "  \"escalated\": true/false,\n"
                "  \"escalation_reason\": \"Short reason string if escalated, otherwise null\"\n"
                "}"
            )
        }
    ]
    
    # Inject historical context
    for msg in session_history[-10:]:  # Keep context window reasonable
        api_messages.append({"role": msg["role"], "content": msg["content"]})
        
    # Append current user message
    api_messages.append({"role": "user", "content": user_message})
    
    try:
        response = openai.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=api_messages,
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        result_text = response.choices[0].message.content
        return json.loads(result_text)
        
    except Exception as e:
        # Fallback to rule-based execution if OpenAI fails (API key issue, timeout, rate limits, etc.)
        print(f"OpenAI API error: {e}. Falling back to Rule-Based Heuristics.")
        return None

def process_chat_message(db: Session, session_id: str, message_text: str) -> Dict[str, Any]:
    """
    The main processing entrypoint for an incoming chat message.
    Updates the session history, runs the conversation logic (LLM or Falling back), 
    applies Lead Qualification updates, saves everything to SQLite, and returns the response.
    """
    # 1. Retrieve or create Session
    chat_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    if not chat_session:
        chat_session = ChatSession(session_id=session_id)
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

    history = json.loads(chat_session.messages)

    # 2. Retrieve or create Lead
    lead = None
    if chat_session.lead_id:
        lead = db.query(Lead).filter(Lead.id == chat_session.lead_id).first()
        
    if not lead:
        lead = Lead()
        db.add(lead)
        db.commit()
        db.refresh(lead)
        chat_session.lead_id = lead.id
        db.commit()

    # 3. Check for direct immediate escalation (Emergency words, frustration, human requests)
    should_escalate, escalation_reason = check_immediate_escalation(message_text)
    if should_escalate:
        lead.escalated = True
        lead.status = "escalated"
        lead.escalation_reason = escalation_reason
        db.commit()
        
        # Immediate safety warning or transfer statement
        if "gas leak" in escalation_reason.lower() or "carbon monoxide" in escalation_reason.lower() or "smoke" in escalation_reason.lower() or "sparks" in escalation_reason.lower():
            response_text = (
                "⚠️ SAFETY WARNING: This sounds like an immediate safety concern. "
                "I have paused autonomous actions and escalated this to our Emergency On-Call Manager. "
                "Please step outside to safety if there is a gas leak or smoke, and a representative will call you immediately."
            )
        else:
            response_text = (
                "I understand completely. I am pausing our automated assistance and transferring you "
                f"directly to one of our friendly office team members right now. They will review our chat and help you immediately."
            )
            
        history.append({"role": "user", "content": message_text})
        history.append({"role": "assistant", "content": response_text})
        chat_session.messages = json.dumps(history)
        chat_session.current_step = "completed"
        db.commit()
        
        return {
            "response_message": response_text,
            "session_id": session_id,
            "current_step": "completed",
            "escalated": True,
            "escalation_reason": escalation_reason,
            "lead": lead
        }

    # 4. Generate next conversation turn using LLM or Fallback Heuristics
    llm_result = None
    if OPENAI_API_KEY:
        # Try running OpenAI
        llm_result = run_openai_agent(message_text, history, lead)
        
    if llm_result:
        # Successfully executed OpenAI
        response_text = llm_result.get("response_message")
        next_step = chat_session.current_step  # Maintain or let database update
        
        # Apply extracted values
        if llm_result.get("first_name"): lead.first_name = llm_result["first_name"]
        if llm_result.get("last_name"): lead.last_name = llm_result["last_name"]
        if llm_result.get("phone"): lead.phone = llm_result["phone"]
        if llm_result.get("email"): lead.email = llm_result["email"]
        if llm_result.get("zip_code"): lead.zip_code = llm_result["zip_code"]
        if llm_result.get("service_needed"): lead.service_needed = llm_result["service_needed"]
        if llm_result.get("service_classification"): lead.service_classification = llm_result["service_classification"]
        if llm_result.get("urgency"): lead.urgency = llm_result["urgency"]
        if llm_result.get("budget_status"): lead.budget_status = llm_result["budget_status"]
        if llm_result.get("appointment_booked") is not None: lead.appointment_booked = llm_result["appointment_booked"]
        if llm_result.get("escalated"):
            lead.escalated = True
            lead.escalation_reason = llm_result.get("escalation_reason") or "LLM requested escalation"
            lead.status = "escalated"
            chat_session.current_step = "completed"
    else:
        # Run Rule-Based fallbacks
        response_text, next_step, extracted = run_rule_based_fallback(
            message_text, history, chat_session.current_step, lead
        )
        
        # Apply extracted
        if "first_name" in extracted: lead.first_name = extracted["first_name"]
        if "last_name" in extracted: lead.last_name = extracted["last_name"]
        if "phone" in extracted: lead.phone = extracted["phone"]
        if "email" in extracted: lead.email = extracted["email"]
        if "zip_code" in extracted: lead.zip_code = extracted["zip_code"]
        if "service_needed" in extracted: lead.service_needed = extracted["service_needed"]
        if "service_classification" in extracted: lead.service_classification = extracted["service_classification"]
        if "urgency" in extracted: lead.urgency = extracted["urgency"]
        if "budget_status" in extracted: lead.budget_status = extracted["budget_status"]
        if "appointment_booked" in extracted: lead.appointment_booked = extracted["appointment_booked"]
        
        chat_session.current_step = next_step

    # 5. Run dynamic Lead Qualification updates (Service classification, Urgency, Service Area checks, Score calculations)
    # Double check classifications via python heuristics if they are null, to ensure we never have empty data
    if not lead.service_classification and lead.service_needed:
        lead.service_classification = heuristic_classify_service(lead.service_needed)
    if not lead.urgency and lead.service_needed:
        lead.urgency = heuristic_classify_urgency(lead.service_needed, lead.service_classification)
    if not lead.budget_status and lead.service_needed:
        lead.budget_status = heuristic_classify_budget(lead.service_needed)

    # Resolve city/state if served ZIP is provided
    if lead.zip_code:
        loc_info = verify_service_area(lead.zip_code)
        if loc_info["is_served"]:
            lead.city = loc_info["city"]
            lead.state = loc_info["state"]

    # Calculate final score
    has_contact = bool(lead.phone or lead.email)
    score = calculate_lead_score(
        service_classification=lead.service_classification,
        urgency=lead.urgency,
        budget_status=lead.budget_status,
        zip_code=lead.zip_code,
        has_contact_info=has_contact,
        appointment_ready=bool(chat_session.current_step == "book_appointment"),
        appointment_booked=bool(lead.appointment_booked)
    )
    lead.lead_score = score
    lead.lead_score_category = get_lead_category(score)

    # Set lead status
    if lead.escalated:
        lead.status = "escalated"
    elif lead.appointment_booked:
        lead.status = "booked"
    elif score >= 80:
        lead.status = "qualified"
    else:
        lead.status = "nurturing"

    # Save messages to history
    history.append({"role": "user", "content": message_text})
    history.append({"role": "assistant", "content": response_text})
    chat_session.messages = json.dumps(history)
    
    db.commit()
    db.refresh(lead)
    db.refresh(chat_session)

    return {
        "response_message": response_text,
        "session_id": session_id,
        "current_step": chat_session.current_step,
        "escalated": lead.escalated,
        "escalation_reason": lead.escalation_reason,
        "lead": lead
    }
