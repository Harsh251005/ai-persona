import requests
from datetime import datetime, timedelta, timezone
from src.config.settings import CAL_API_KEY, CAL_USERNAME, CAL_EVENT_SLUG

CAL_BASE_URL = "https://api.cal.com/v2"

# IMPORTANT: Cal.com v2 uses DIFFERENT version headers per endpoint group
# Slots:    2024-09-04
# Bookings: 2024-08-13
# Using wrong version = 404

def _headers(version: str) -> dict:
    return {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "cal-api-version": version,
        "Content-Type": "application/json",
    }


def check_cal_availability(
    start_time: str | None = None,
    end_time: str | None = None,
    timezone: str = "Asia/Kolkata",
) -> dict:
    """
    Fetch available slots from Cal.com using username + eventTypeSlug.
    No numeric event type ID required.

    Returns:
        {
            "available": bool,
            "slots": { "2026-06-09": ["2026-06-09T03:30:00.000Z", ...] },
            "error": str | None
        }
    """
    now = datetime.now(tz=_utc())
    if not start_time:
        start_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    if not end_time:
        end_time = (now + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

    params = {
        "username": CAL_USERNAME,
        "eventTypeSlug": CAL_EVENT_SLUG,
        "start": start_time,
        "end": end_time,
        "timeZone": timezone,
    }

    try:
        response = requests.get(
            f"{CAL_BASE_URL}/slots",
            headers=_headers("2024-09-04"),  # slots version
            params=params,
            timeout=10,
        )
        print(f"[CAL DEBUG slots] {response.status_code}: {response.text[:300]}")
        response.raise_for_status()
        data = response.json()

        # Response shape: { "data": { "2026-06-09": [{"start": "..."}, ...] } }
        raw: dict = data.get("data", {})

        flat_slots = {}
        for date_str, slot_list in raw.items():
            if isinstance(slot_list, list):
                flat_slots[date_str] = [
                    s["start"] if isinstance(s, dict) else s
                    for s in slot_list
                ]

        return {
            "available": bool(flat_slots),
            "slots": flat_slots,
            "error": None,
        }

    except requests.HTTPError as e:
        print(f"[CAL DEBUG slots ERROR] {e.response.status_code}: {e.response.text}")
        return {"available": False, "slots": {}, "error": f"{e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"available": False, "slots": {}, "error": str(e)}


def execute_cal_booking(
    name: str,
    email: str,
    start_time_iso: str,
    timezone: str = "Asia/Kolkata",
    notes: str = "",
) -> dict:
    """
    Book a meeting. Uses username + eventTypeSlug in payload.
    start_time_iso must be an exact slot string from check_cal_availability.

    Returns:
        {
            "success": bool,
            "booking_uid": str | None,
            "booking_url": str | None,
            "start": str | None,
            "end": str | None,
            "error": str | None
        }
    """
    payload = {
        "username": CAL_USERNAME,
        "eventTypeSlug": CAL_EVENT_SLUG,
        "start": start_time_iso,
        "attendee": {
            "name": name,
            "email": email,
            "timeZone": timezone,
        },
    }

    if notes:
        payload["bookingFieldsResponses"] = {"notes": notes}

    try:
        response = requests.post(
            f"{CAL_BASE_URL}/bookings",
            headers=_headers("2024-08-13"),  # bookings version
            json=payload,
            timeout=10,
        )
        print(f"[CAL DEBUG booking] {response.status_code}: {response.text[:300]}")
        response.raise_for_status()
        data = response.json().get("data", {})

        return {
            "success": True,
            "booking_uid": data.get("uid"),
            "booking_url": data.get("meetingUrl") or data.get("videoCallUrl"),
            "start": data.get("start"),
            "end": data.get("end"),
            "error": None,
        }

    except requests.HTTPError as e:
        print(f"[CAL DEBUG booking ERROR] {e.response.status_code}: {e.response.text}")
        return {
            "success": False,
            "booking_uid": None,
            "booking_url": None,
            "start": None,
            "end": None,
            "error": f"{e.response.status_code}: {e.response.text}",
        }
    except Exception as e:
        return {"success": False, "booking_uid": None, "booking_url": None, "start": None, "end": None, "error": str(e)}


def cancel_cal_booking(
    booking_uid: str,
    reason: str = "Cancelled via AI assistant",
) -> dict:
    """Cancel an existing booking by uid."""
    try:
        response = requests.post(
            f"{CAL_BASE_URL}/bookings/{booking_uid}/cancel",
            headers=_headers("2024-08-13"),  # bookings version
            json={"cancellationReason": reason},
            timeout=10,
        )
        print(f"[CAL DEBUG cancel] {response.status_code}: {response.text[:300]}")
        response.raise_for_status()
        return {"success": True, "error": None}

    except requests.HTTPError as e:
        return {"success": False, "error": f"{e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _utc():
    return timezone.utc