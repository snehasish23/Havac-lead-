import re
from typing import Dict, Any, Optional

# Predefined Service Area for Austin, TX region
SERVED_ZIP_CODES = {
    # Austin, TX core
    "78701": {"city": "Austin", "state": "TX", "tier": "core", "distance": 2},
    "78702": {"city": "Austin", "state": "TX", "tier": "core", "distance": 3},
    "78703": {"city": "Austin", "state": "TX", "tier": "core", "distance": 4},
    "78704": {"city": "Austin", "state": "TX", "tier": "core", "distance": 3},
    "78705": {"city": "Austin", "state": "TX", "tier": "core", "distance": 5},
    "78712": {"city": "Austin", "state": "TX", "tier": "core", "distance": 6},
    "78721": {"city": "Austin", "state": "TX", "tier": "core", "distance": 7},
    "78723": {"city": "Austin", "state": "TX", "tier": "core", "distance": 6},
    "78741": {"city": "Austin", "state": "TX", "tier": "core", "distance": 5},
    "78745": {"city": "Austin", "state": "TX", "tier": "core", "distance": 8},
    "78746": {"city": "Austin", "state": "TX", "tier": "core", "distance": 7},
    "78751": {"city": "Austin", "state": "TX", "tier": "core", "distance": 4},
    "78752": {"city": "Austin", "state": "TX", "tier": "core", "distance": 5},
    "78753": {"city": "Austin", "state": "TX", "tier": "core", "distance": 9},
    "78757": {"city": "Austin", "state": "TX", "tier": "core", "distance": 6},
    "78758": {"city": "Austin", "state": "TX", "tier": "core", "distance": 8},
    "78759": {"city": "Austin", "state": "TX", "tier": "core", "distance": 9},
    # Round Rock, TX
    "78664": {"city": "Round Rock", "state": "TX", "tier": "nearby", "distance": 18},
    "78665": {"city": "Round Rock", "state": "TX", "tier": "nearby", "distance": 20},
    "78681": {"city": "Round Rock", "state": "TX", "tier": "nearby", "distance": 22},
    # Pflugerville, TX
    "78660": {"city": "Pflugerville", "state": "TX", "tier": "nearby", "distance": 15},
    # Cedar Park, TX
    "78613": {"city": "Cedar Park", "state": "TX", "tier": "nearby", "distance": 19}
}

VALID_SERVICE_CLASSIFICATIONS = [
    "AC Repair", "AC Installation", "Furnace Repair", "Furnace Installation", 
    "Heat Pump", "IAQ", "Maintenance", "Emergency"
]

def verify_service_area(zip_code: Optional[str]) -> Dict[str, Any]:
    """
    Verifies if a ZIP code is within the active HVAC service area.
    """
    if not zip_code:
        return {
            "is_served": False,
            "city": None,
            "state": None,
            "tier": "unknown",
            "distance_miles": None,
            "message": "ZIP code not provided."
        }
    
    clean_zip = str(zip_code).strip()
    if clean_zip in SERVED_ZIP_CODES:
        info = SERVED_ZIP_CODES[clean_zip]
        tier = info["tier"]
        distance = info["distance"]
        
        if tier == "core":
            message = "We serve this neighborhood daily! Standard dispatch rates apply."
        else:
            message = "We service this area with an extended dispatch tier."
            
        return {
            "is_served": True,
            "city": info["city"],
            "state": info["state"],
            "tier": tier,
            "distance_miles": distance,
            "message": message
        }
    
    # Try to recognize basic format
    if re.match(r"^\d{5}$", clean_zip):
        return {
            "is_served": False,
            "city": None,
            "state": None,
            "tier": "unsupported",
            "distance_miles": 60,
            "message": f"Sorry, ZIP code {clean_zip} is currently outside our service area."
        }
    else:
        return {
            "is_served": False,
            "city": None,
            "state": None,
            "tier": "invalid",
            "distance_miles": None,
            "message": "Invalid ZIP code format."
        }

def heuristic_classify_service(text: str) -> str:
    """
    Classify service needed from raw conversational text using keyword heuristics.
    """
    text_lower = text.lower()
    
    # 1. Emergency keywords first
    emergency_patterns = [
        r"\bgas leak\b", r"\bcarbon monoxide\b", r"\bco leak\b", r"\bsmoke\b", 
        r"\bsparks\b", r"\belectrical spark\b", r"\bfire\b", r"\bflooding\b"
    ]
    for pattern in emergency_patterns:
        if re.search(pattern, text_lower):
            return "Emergency"

    # 2. Heat Pump
    if "heat pump" in text_lower or "heatpump" in text_lower:
        return "Heat Pump"

    # 3. Furnace Install vs Furnace Repair (Heating specific keywords)
    if any(k in text_lower for k in ["new furnace", "replace furnace", "install furnace", "furnace install", "new heater", "replace heater", "furnace replacement", "heater replacement", "heater installation"]):
        return "Furnace Installation"
        
    if any(k in text_lower for k in ["furnace repair", "heater repair", "heater broken", "no heat", "not heating", "furnace issue", "furnace blowing cold", "thermostat broken", "heater is broken", "heater leaking", "heater is leaking", "furnace won't", "furnace", "heater", "heating"]):
        return "Furnace Repair"

    # 4. AC Install vs AC Repair (AC specific keywords)
    if any(k in text_lower for k in [
        "new ac", "replace ac", "replace air", "install ac", "ac install", "ac quote", 
        "new system", "system replacement", "new air conditioner", "replace air conditioner", 
        "install air conditioner", "air conditioner replacement", "quote on a", "quote for",
        "new unit", "replace unit", "install unit"
    ]):
        return "AC Installation"
    
    if any(k in text_lower for k in ["ac repair", "blowing warm", "not cooling", "ac broken", "air conditioner leak", "freon", "condenser", "compressor", "air conditioning issue", "ac is leaking", "air conditioner"]):
        return "AC Repair"
        
    # 5. IAQ
    if any(k in text_lower for k in ["air filter", "iaq", "air purifier", "allergen", "humidity", "dehumidifier", "uv light", "indoor air"]):
        return "IAQ"
        
    # 6. Maintenance
    if any(k in text_lower for k in ["maintenance", "tune up", "tune-up", "spring clean", "winterize", "yearly check", "membership", "service contract"]):
        return "Maintenance"
        
    return "AC Repair"  # Default fallback service needed for HVAC leads

def heuristic_classify_urgency(text: str, service_type: str) -> str:
    """
    Classify urgency from raw conversational text and service type.
    """
    if service_type == "Emergency":
        return "Hot"
        
    text_lower = text.lower()
    
    # Hot indicators: no cooling/heating in extreme weather, water leaking through ceiling
    hot_indicators = [
        "emergency", "no ac", "no cooling", "no heat", "not heating", "blowing hot", "blowing warm",
        "freezing", "hot in here", "leaking water", "active leak", "asap", "today", "tonight", "right away"
    ]
    if any(k in text_lower for k in hot_indicators):
        return "Hot"
        
    # Warm indicators: planning, scheduling soon, quote comparisons
    warm_indicators = [
        "schedule", "next week", "quote", "estimate", "replace soon", "getting quotes", "price comparison",
        "not urgent", "diagnostic", "working but", "making noise"
    ]
    if any(k in text_lower for k in warm_indicators):
        return "Warm"
        
    # Cold indicators: researching, asking general questions
    cold_indicators = [
        "researching", "just checking", "future", "next year", "how much", "typical cost", "general question"
    ]
    if any(k in text_lower for k in cold_indicators):
        return "Cold"
        
    return "Warm"  # Default fallback

def heuristic_classify_budget(text: str) -> str:
    """
    Classify budget qualification status from text.
    """
    text_lower = text.lower()
    
    if any(k in text_lower for k in ["buy now", "asap", "schedule today", "ready to go", "don't care about cost", "get it fixed", "ready to buy", "buy a new", "buy today"]):
        return "Ready to buy"
        
    if any(k in text_lower for k in ["financing", "finance", "payment plan", "payments", "credit card", "loan"]):
        return "Needs financing"
        
    if any(k in text_lower for k in ["quote", "estimate", "shopping", "comparing", "price match", "how much"]):
        return "Comparing"
        
    return "Unknown"

def calculate_lead_score(
    service_classification: Optional[str],
    urgency: Optional[str],
    budget_status: Optional[str],
    zip_code: Optional[str],
    has_contact_info: bool,
    appointment_ready: bool,
    appointment_booked: bool
) -> int:
    """
    Calculate Lead Score dynamically from 0 to 100.
    
    Scoring components:
    - Service / Intent: Max 20 points
    - Urgency: Max 30 points
    - Budget Match: Max 20 points
    - Location verification: Max 20 points
    - Contact / Ready State: Max 10 points (additional booked bonus)
    """
    score = 0
    
    # 1. Service / Intent (Max 20)
    service_scores = {
        "Emergency": 20,
        "AC Installation": 20,
        "Furnace Installation": 20,
        "Heat Pump": 20,
        "AC Repair": 15,
        "Furnace Repair": 15,
        "IAQ": 10,
        "Maintenance": 10,
        None: 5
    }
    score += service_scores.get(service_classification, 5)
    
    # 2. Urgency (Max 30)
    urgency_scores = {
        "Hot": 30,
        "Warm": 15,
        "Cold": 5,
        None: 5
    }
    score += urgency_scores.get(urgency, 5)
    
    # 3. Budget Status (Max 20)
    budget_scores = {
        "Ready to buy": 20,
        "Needs financing": 15,
        "Comparing": 10,
        "Unknown": 5,
        None: 5
    }
    score += budget_scores.get(budget_status, 5)
    
    # 4. Location Verification (Max 20)
    loc_info = verify_service_area(zip_code)
    if loc_info["is_served"]:
        if loc_info["tier"] == "core":
            score += 20
        else:
            score += 15
    else:
        # Out of area leads get zeroed on location
        score += 0
        
    # 5. Contact Info & Ready state (Max 10)
    if has_contact_info:
        score += 5
    if appointment_ready or appointment_booked:
        score += 5
        
    # Score bounding
    score = max(0, min(100, score))
    return score

def get_lead_category(score: int) -> str:
    """
    Categorizes the lead score into standard follow-up buckets:
    - 80-100: Hot (book immediately)
    - 50-79: Warm (nurture)
    - 0-49: Cold (long-term nurture)
    """
    if score >= 80:
        return "Hot"
    elif score >= 50:
        return "Warm"
    else:
        return "Cold"
