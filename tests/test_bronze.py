import json

from pyspark.sql import functions as F

from open_text_corpus_pipeline.ingest.bronze import add_bronze_columns, ingest_jsonl
from open_text_corpus_pipeline.manifest import REQUIRED_KEYS, build_manifest, write_manifest


def _raw_df(spark, rows):
    return spark.createDataFrame(rows, ["source_id", "url", "title", "text"])


def test_content_hash_is_deterministic(spark):
    df = _raw_df(spark, [
        ("1", "u", "t", "Hello world"),
        ("2", "u", "t", "Hello world"),
    ])
    hashes = [r.content_hash for r in add_bronze_columns(df).collect()]
    assert hashes[0] == hashes[1]
    assert len(hashes[0]) == 64


def test_one_character_change_changes_hash(spark):
    df = _raw_df(spark, [
        ("1", "u", "t", "Hello world"),
        ("2", "u", "t", "Hello worle"),
    ])
    hashes = [r.content_hash for r in add_bronze_columns(df).collect()]
    assert hashes[0] != hashes[1]


def test_doc_id_is_stable_across_runs(spark):
    df = _raw_df(spark, [("42", "u", "t", "text")])
    first = add_bronze_columns(df).select("doc_id").first().doc_id
    second = add_bronze_columns(df).select("doc_id").first().doc_id
    assert first == second


def test_ingest_output_has_no_null_or_duplicate_ids(spark, tmp_path):
    input_path = tmp_path / "in.jsonl"
    records = [
        {"source_id": str(i), "url": "u", "title": f"t{i}", "text": f"body {i}"}
        for i in range(50)
    ]
    input_path.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")

    output_path = tmp_path / "bronze"
    rows = ingest_jsonl(spark, str(input_path), str(output_path))
    out = spark.read.parquet(str(output_path))

    assert rows == 50
    assert out.filter(F.col("doc_id").isNull()).count() == 0
    assert out.select("doc_id").distinct().count() == out.count()


def test_manifest_contains_required_keys(tmp_path):
    manifest = build_manifest("src", "in.jsonl", "out", rows_in=10, rows_out=10)
    assert set(manifest) >= REQUIRED_KEYS
    path = write_manifest(manifest, tmp_path / "m.json")
    assert json.loads(path.read_text(encoding="utf-8"))["rows_out"] == 10


def test_manifest_rejects_missing_keys(tmp_path):
    import pytest

    with pytest.raises(ValueError, match="missing keys"):
        write_manifest({"source": "x"}, tmp_path / "bad.json")