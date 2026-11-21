"""Quality filters for Silver. Each filter marks a document as kept or removed."""

MIN_CHARS = 200
MAX_CHARS = 100_000


def passes_length(text: str | None, min_chars: int = MIN_CHARS, max_chars: int = MAX_CHARS) -> bool:
    """Return True if the text length is within bounds. Null text fails."""
    if text is None:
        return False
    return min_chars <= len(text) <= max_chars