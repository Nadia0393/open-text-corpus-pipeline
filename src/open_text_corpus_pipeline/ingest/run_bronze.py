"""Run the Bronze ingestion end to end."""

import logging

from pyspark.sql import SparkSession

from open_text_corpus_pipeline.ingest.bronze import ingest_jsonl

INPUT = "data/raw/wikipedia_sample.jsonl"
OUTPUT = "data/bronze/wikipedia"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("bronze")


def main() -> None:
    spark = SparkSession.builder.master("local[*]").appName("bronze").getOrCreate()
    try:
        rows = ingest_jsonl(spark, INPUT, OUTPUT)
        log.info("Wrote %d rows to %s", rows, OUTPUT)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
