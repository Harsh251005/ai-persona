"""
intent_detector.py

Lightweight keyword-based intent classifier.
Runs BEFORE the LLM call to give the orchestrator a routing hint.
The LLM still makes the final tool-call decision — this is just a fast pre-filter
useful for logging, analytics, or future routing logic.
"""

import re

# ---------------------------------------------------------------------------
# Keyword sets
# ---------------------------------------------------------------------------

_BOOKING_KEYWORDS = {
    "book", "schedule", "meeting", "call", "appointment",
    "slot", "availability", "available", "free", "busy",
    "calendar", "catch up", "sync", "chat", "zoom", "meet",
    "reserve", "block", "confirm", "set up a time",
}

_CANCEL_KEYWORDS = {
    "cancel", "cancellation", "reschedule", "postpone",
    "unbook", "remove booking", "delete meeting",
}

_PORTFOLIO_KEYWORDS = {
    "project", "experience", "skill", "resume", "work",
    "built", "tech stack", "rag", "langchain", "qdrant",
    "education", "college", "degree", "background", "about",
    "github", "evidently", "evidentai", "truthlens", "insightforge",
    "python", "fastapi", "langraph", "groq", "openai",
}


def _tokenize(text: str) -> set[str]:
    """Lowercase + split on non-word characters."""
    return set(re.split(r"\W+", text.lower()))


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

INTENT_BOOKING = "booking"
INTENT_CANCEL = "cancel"
INTENT_PORTFOLIO = "portfolio"
INTENT_UNKNOWN = "unknown"


def detect_intent(query: str) -> str:
    """
    Returns one of: 'booking', 'cancel', 'portfolio', 'unknown'.

    Priority order: cancel > booking > portfolio > unknown
    (cancel is more specific so checked first)
    """
    tokens = _tokenize(query)

    if tokens & _CANCEL_KEYWORDS:
        return INTENT_CANCEL

    if tokens & _BOOKING_KEYWORDS:
        return INTENT_BOOKING

    if tokens & _PORTFOLIO_KEYWORDS:
        return INTENT_PORTFOLIO

    return INTENT_UNKNOWN


def is_calendar_intent(query: str) -> bool:
    """Convenience check — True if booking OR cancel intent."""
    intent = detect_intent(query)
    return intent in (INTENT_BOOKING, INTENT_CANCEL)


def is_portfolio_intent(query: str) -> bool:
    """Convenience check — True if portfolio intent."""
    return detect_intent(query) == INTENT_PORTFOLIO