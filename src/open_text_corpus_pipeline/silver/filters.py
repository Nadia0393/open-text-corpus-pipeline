"""Quality filters for Silver. Each filter marks a document as kept or removed."""

MIN_CHARS = 200
MAX_CHARS = 100_000


def passes_length(text: str | None, min_chars: int = MIN_CHARS, max_chars: int = MAX_CHARS) -> bool:
    """Return True if the text length is within bounds. Null text fails."""
    if text is None:
        return False
    return min_chars <= len(text) <= max_chars

MAX_NON_ALNUM_RATIO = 0.3


def passes_non_alnum_ratio(text: str | None, max_ratio: float = MAX_NON_ALNUM_RATIO) -> bool:
    """Return True if the share of symbol characters is at or below max_ratio.

    Letters, digits, and whitespace are not counted. Null or empty text fails.
    """
    if not text:
        return False
    symbols = sum(1 for ch in text if not ch.isalnum() and not ch.isspace())
    return symbols / len(text) <= max_ratio