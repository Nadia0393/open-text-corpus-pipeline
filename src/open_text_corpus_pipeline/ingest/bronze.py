"""Bronze layer: raw JSONL in, partitioned Parquet out."""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

DEFAULT_SOURCE = "wikipedia-20231101-en"


def add_bronze_columns(df: DataFrame, source: str = DEFAULT_SOURCE) -> DataFrame:
    """Add the stable identifiers and metadata every Bronze row needs.

    doc_id is derived from the source's own article ID, so rerunning on the
    same input produces the same IDs. content_hash is a SHA-256 of the text,
    so any change to the article body is detectable.
    """
    return (
        df.withColumn("doc_id", F.concat_ws(":", F.lit(source), F.col("source_id")))
        .withColumn("content_hash", F.sha2(F.col("text"), 256))
        .withColumn("source", F.lit(source))
        .withColumn("ingested_at", F.current_timestamp())
        .withColumn("ingest_date", F.to_date(F.col("ingested_at")))
    )


def ingest_jsonl(
    spark: SparkSession,
    input_path: str,
    output_path: str,
    source: str = DEFAULT_SOURCE,
) -> int:
    """Read JSONL, write Bronze Parquet partitioned by ingest date, return row count."""
    raw = spark.read.json(input_path)
    bronze = add_bronze_columns(raw, source)
    bronze.write.mode("overwrite").partitionBy("ingest_date").parquet(output_path)
    return spark.read.parquet(output_path).count()
