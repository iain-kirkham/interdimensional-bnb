from datetime import timedelta


def apply_time_dilation(booking):
    """
    Takes a Booking instance and returns a dict containing:
    - adjusted_nights
    - adjusted_checkout
    - warnings (optional)
    """
    rules = booking.room.reality_rules or {}
    time_rules = rules.get("time", {})

    factor = time_rules.get("dilation_factor", 1)
    offset_hours = time_rules.get("offset_hours", 0)

    adjusted_nights = booking.nights * factor

    adjusted_checkout = (
        booking.check_in +
        timedelta(days=adjusted_nights) +
        timedelta(hours=offset_hours)
    )

    return {
        "adjusted_nights": adjusted_nights,
        "adjusted_checkout": adjusted_checkout,
        "warnings": rules.get("warnings", []),
        "physics": rules.get("physics", {})
    }
