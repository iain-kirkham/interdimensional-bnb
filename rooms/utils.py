from datetime import datetime, time, timedelta


def apply_time_dilation(booking):
    """
    Computes dimension-adjusted stay details for a Booking instance.

    Uses the room's reality_rules JSON to apply:
    - time.dilation_factor: multiplier for nights (default: 1)
    - time.offset_hours: additional hours added to checkout (default: 0)

    Converts booking.check_in (a date) into a datetime at midnight before
    applying timedelta adjustments, ensuring hour-level precision.

    Returns a dict containing:
    - adjusted_nights (float)
    - adjusted_checkout (datetime)
    - warnings (list of strings)
    - physics (dict of optional flavour metadata)
    """

    rules = booking.room.reality_rules or {}
    time_rules = rules.get("time", {})

    factor = time_rules.get("dilation_factor", 1)
    offset_hours = time_rules.get("offset_hours", 0)

    # Calculate adjusted nights
    adjusted_nights = booking.nights * factor

    # Promote check_in (a date) to a datetime at midnight
    base_dt = datetime.combine(booking.check_in, time.min)

    # Add days and hours
    adjusted_checkout = base_dt + timedelta(
            days=adjusted_nights,
            hours=offset_hours,
    )

    return {
        "adjusted_nights": adjusted_nights,
        "adjusted_checkout": adjusted_checkout,
        "warnings": rules.get("warnings", []),
        "physics": rules.get("physics", {})
    }
