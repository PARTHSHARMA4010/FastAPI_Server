# extractor.py

from typing import List, Dict, Optional

# Define question keyword maps for fuzzy matching
keywords = {
    "schedule": {
        "early": "Early bird",
        "moderate": "Moderate",
        "night": "Night owl"
    },
    "tidiness": {
        "super": "Super organized",
        "somewhat": "Somewhat tidy",
        "messy": "Not very tidy"
    },
    "environment": {
        "silence": "Need complete silence",
        "quiet": "Need complete silence",
        "noise": "Some background noise is okay",
        "okay": "Some background noise is okay"
    },
    "cooking": {
        "daily": "Cook daily at home",
        "3": "Cook 3–4 times per week",
        "times": "Cook 3–4 times per week",
        "order": "Mostly order in/eat out",
        "eat out": "Mostly order in/eat out"
    },
    "work_mode": {
        "home": "Always work/study from home",
        "mix": "Mix of home and outside",
        "library": "Prefer libraries/cafes/office",
        "office": "Prefer libraries/cafes/office",
        "cafe": "Prefer libraries/cafes/office"
    },
    "stress": {
        "talk": "Talk it out with others",
        "space": "Need some space first, then talk",
        "alone": "Prefer to handle alone",
        "myself": "Prefer to handle alone"
    },
    "personality": {
        "introvert": "Introvert (prefer solitude)",
        "ambivert": "Ambivert (balanced social needs)",
        "extrovert": "Extrovert (love social interaction)"
    },
    "conversation": {
        "regular": "Love regular chats and bonding",
        "bond": "Love regular chats and bonding",
        "occasion": "Occasional friendly conversation",
        "privacy": "Prefer privacy and minimal interaction",
        "minimal": "Prefer privacy and minimal interaction"
    },
    "conflict": {
        "address": "Address immediately and talk it out",
        "discuss": "Take time to think, then discuss",
        "think": "Take time to think, then discuss",
        "avoid": "Prefer to avoid direct conflict"
    },
    "celebration": {
        "celebrating together": "Love celebrating together",
        "together": "Love celebrating together",
        "occasion": "Occasional small celebrations",
        "low": "Prefer to keep things low-key",
        "quiet": "Prefer to keep things low-key"
    },
    "floor": {
        "ground": "Ground floor (easy access)",
        "middle": "Middle floors (balanced)",
        "top": "Top floor (better view/privacy)"
    },
    "spot": {
        "window": "Near window (natural light)",
        "door": "Near door (easy access)",
        "no preference": "No preference",
        "anywhere": "No preference"
    },
    "sunlight": {
        "sunny": "Sunny room (lots of natural light)",
        "light": "Sunny room (lots of natural light)",
        "moderate": "Moderate sunlight",
        "shade": "Shaded/cooler room",
        "cool": "Shaded/cooler room"
    }
}

def find_match(answer: str, keyword_dict: dict) -> Optional[str]:
    """Searches for matching keyword in answer string and maps to clean label."""
    answer = answer.lower()
    for k, v in keyword_dict.items():
        if k in answer:
            return v
    return None

def extract_responses(username: str, conversation: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Extracts structured roommate preference data from a list of Q&A.
    
    Parameters:
        username: str — email or user name
        conversation: list of dicts — [{"question": str, "answer": str}, ...]

    Returns:
        dict of extracted profile values
    """
    profile = {
        "username": username
    }

    field_order = list(keywords.keys())
    idx = 0

    for conv in conversation:
        if idx >= len(field_order):
            break
        field = field_order[idx]
        match = find_match(conv["answer"], keywords[field])
        if match:
            profile[field] = match
        idx += 1

    return profile
