"""Silver normalization: Unicode and whitespace cleanup for article text."""

import re
import unicodedata

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

_SPACES = re.compile(r"[ \t\u00a0]+")
_BLANK_RUNS = re.compile(r"\n{3,}")


def normalize_text(text: str | None) -> str | None:
    """Return NFC-normalized text with consistent line endings and whitespace.

    Pure Python, so it can be tested without Spark. Null input stays null.
    """
    if text is None:
        return None
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [_SPACES.sub(" ", line).strip() for line in text.split("\n")]
    text = "\n".join(lines)
    text = _BLANK_RUNS.sub("\n\n", text)
    return text.strip()


def add_normalized_text(df: DataFrame) -> DataFrame:
    """Add text_normalized alongside the untouched raw text column."""
    normalize_udf = F.udf(normalize_text, StringType())
    return df.withColumn("text_normalized", normalize_udf(F.col("text")))