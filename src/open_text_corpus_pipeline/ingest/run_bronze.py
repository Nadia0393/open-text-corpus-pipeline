"""Run the Bronze ingestion end to end and write a manifest."""

import logging
from datetime import date

from pyspark.sql import SparkSession

from open_text_corpus_pipeline.ingest.bronze import DEFAULT_SOURCE, ingest_jsonl
from open_text_corpus_pipeline.manifest import build_manifest, write_manifest

INPUT = "data/raw/wikipedia_sample.jsonl"
OUTPUT = "data/bronze/wikipedia"
MANIFEST_DIR = "data/manifests"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("bronze")


def count_lines(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f)


def main() -> None:
    rows_in = count_lines(INPUT)
    spark = SparkSession.builder.master("local[*]").appName("bronze").getOrCreate()
    try:
        rows_out = ingest_jsonl(spark, INPUT, OUTPUT)
    finally:
        spark.stop()

    manifest = build_manifest(DEFAULT_SOURCE, INPUT, OUTPUT, rows_in, rows_out)
    path = write_manifest(manifest, f"{MANIFEST_DIR}/bronze-{date.today().isoformat()}.json")
    log.info("Rows in=%d out=%d, manifest at %s", rows_in, rows_out, path)


if __name__ == "__main__":
    main()