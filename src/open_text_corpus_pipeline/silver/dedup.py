"""Exact deduplication: keep one row per normalized-text hash."""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def add_normalized_hash(df: DataFrame) -> DataFrame:
    """Add normalized_hash, the SHA-256 of text_normalized. Null text gives a null hash."""
    return df.withColumn("normalized_hash", F.sha2(F.col("text_normalized"), 256))


def dedup_exact(df: DataFrame) -> DataFrame:
    """Keep one row per normalized_hash, choosing the lowest doc_id.

    Rows with a null hash are dropped first, because nulls would otherwise
    collapse into a single row. Choosing by doc_id makes reruns deterministic.
    """
    present = df.filter(F.col("normalized_hash").isNotNull())
    window = Window.partitionBy("normalized_hash").orderBy("doc_id")
    return (
        present.withColumn("_rn", F.row_number().over(window))
        .filter(F.col("_rn") == 1)
        .drop("_rn")
    )