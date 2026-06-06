from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# OpenAI Function Tool Schemas
# These are passed to client.chat.completions.create(tools=[...])
# ---------------------------------------------------------------------------

cal_availability_tool = {
    "type": "function",
    "function": {
        "name": "check_cal_availability",
        "description": (
            "Check Harsh's real-time calendar availability on Cal.com. "
            "Call this BEFORE booking to find open time slots. "
            "Returns a dict of dates → list of available ISO start times."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": (
                        "Start of the search window in ISO 8601 UTC format. "
                        "e.g. '2025-06-10T00:00:00Z'. "
                        "If the user says 'this week' or 'next week', compute accordingly. "
                        "Defaults to today if omitted."
                    ),
                },
                "end_time": {
                    "type": "string",
                    "description": (
                        "End of the search window in ISO 8601 UTC format. "
                        "e.g. '2025-06-17T23:59:59Z'. "
                        "Defaults to 7 days from start_time if omitted."
                    ),
                },
                "timezone": {
                    "type": "string",
                    "description": (
                        "IANA timezone string for the guest. "
                        "e.g. 'Asia/Kolkata', 'America/New_York'. "
                        "Defaults to 'Asia/Kolkata'."
                    ),
                },
            },
            "required": [],
        },
    },
}

cal_booking_tool = {
    "type": "function",
    "function": {
        "name": "execute_cal_booking",
        "description": (
            "Book a meeting with Harsh on Cal.com. "
            "ONLY call this after check_cal_availability confirms the slot is open "
            "AND you have collected the guest's name and email. "
            "Returns booking_uid (save this — needed for cancellation), meeting URL, and confirmed time."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Full name of the person booking the meeting.",
                },
                "email": {
                    "type": "string",
                    "description": "Email address of the person booking the meeting.",
                },
                "start_time_iso": {
                    "type": "string",
                    "description": (
                        "Exact slot ISO string from check_cal_availability output. "
                        "e.g. '2025-06-10T10:00:00+05:30'"
                    ),
                },
                "timezone": {
                    "type": "string",
                    "description": "Guest's IANA timezone. e.g. 'Asia/Kolkata'.",
                },
                "notes": {
                    "type": "string",
                    "description": "Optional: reason for the meeting or topics to discuss.",
                },
            },
            "required": ["name", "email", "start_time_iso"],
        },
    },
}

cal_cancel_tool = {
    "type": "function",
    "function": {
        "name": "cancel_cal_booking",
        "description": (
            "Cancel an existing meeting that was booked with Harsh. "
            "Requires the booking_uid returned at booking time. "
            "Ask the user for their booking_uid if not present in conversation history."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "booking_uid": {
                    "type": "string",
                    "description": "The unique booking ID returned when the meeting was created.",
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for cancellation. Optional.",
                },
            },
            "required": ["booking_uid"],
        },
    },
}


def get_calendar_system_prompt() -> str:
    """
    Returns the calendar-specific instructions injected into the system prompt.
    Includes current UTC time so the LLM can reason about relative dates correctly.
    """
    now_utc = datetime.now(tz=timezone.utc)
    now_ist = now_utc.astimezone(
        # IST = UTC+5:30, using fixed offset since no pytz dependency
        timezone(offset=__import__("datetime").timedelta(hours=5, minutes=30))
    )

    return f"""
---
CALENDAR ASSISTANT RULES (follow strictly):

Current date/time:
  UTC: {now_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC
  IST: {now_ist.strftime('%Y-%m-%d %H:%M:%S')} IST

Booking flow — always follow this exact sequence:
  1. If the user wants to schedule a meeting → call check_cal_availability first.
  2. Present the available slots clearly (date + time in the user's timezone).
  3. Ask the user to pick a slot IF they haven't specified one.
  4. Collect name and email IF not already provided in conversation.
  5. Call execute_cal_booking with the confirmed slot, name, and email.
  6. Return the booking confirmation: date, time, meeting URL, and booking_uid.
  7. Tell the user to SAVE their booking_uid — they'll need it to cancel.

Cancellation flow:
  1. Ask for booking_uid if not in context.
  2. Call cancel_cal_booking with the uid.
  3. Confirm cancellation to the user.

Do NOT:
  - Book a meeting without first checking availability.
  - Assume any slot is free without calling check_cal_availability.
  - Invent or guess booking IDs.
  - Book without name + email — always ask if missing.
---
"""