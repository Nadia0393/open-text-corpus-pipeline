"""Quality filters for Silver. Each filter marks a document as kept or removed."""

from collections import Counter

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

MAX_REPEATED_NGRAM_FRACTION=0.2

def repeated_ngram_fraction(text: str, n: int = 3) -> float:
    """Return the share of word n-grams that occur more than once.

    Text shorter than n words returns 0.0, since there is nothing to repeat.
    """
    words = text.split()
    if len(words) < n:
        return 0.0
    grams = [tuple(words[i : i + n]) for i in range(len(words) - n + 1)]
    counts = Counter(grams)
    repeated = sum(c for c in counts.values() if c > 1)
    return repeated / len(grams)


def passes_repeated_ngrams(
    text: str | None,
    max_fraction: float = MAX_REPEATED_NGRAM_FRACTION,
    n: int = 3,
) -> bool:
    """Return True if repeated n-grams make up at most max_fraction of the text.

    Null or empty text fails.
    """
    if not text:
        return False
    return repeated_ngram_fraction(text, n) <= max_fraction