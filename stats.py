"""Statistics and percentile calculation functions."""


def calculate_percentile(value, all_values):
    """Calculate what percentile a value falls into."""
    if not all_values:
        return 0

    count_below = sum(1 for v in all_values if v < value)
    percentile = (count_below / len(all_values)) * 100

    return percentile


def get_rating(percentile):
    """Convert percentile to rating (Bad, OK, Good)."""
    if percentile < 50:
        return "No"
    elif percentile < 80:
        return "Maybe"
    else:
        return "Yes"


def get_rating_color(rating):
    """Get color for rating."""
    if rating == "No":
        return "red"
    elif rating == "Maybe":
        return "orange"
    else:
        return "green"
