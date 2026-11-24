from open_text_corpus_pipeline.silver.dedup import add_normalized_hash, dedup_exact
from open_text_corpus_pipeline.silver.normalize import add_normalized_text


def _prepared(spark, rows):
    df = spark.createDataFrame(rows, ["doc_id", "text"])
    return add_normalized_hash(add_normalized_text(df))


def test_identical_text_collapses_to_one_row(spark):
    df = _prepared(spark, [("a", "same text"), ("b", "same text"), ("c", "other text")])
    out = dedup_exact(df)
    assert out.count() == 2


def test_whitespace_variants_are_duplicates(spark):
    df = _prepared(spark, [("a", "one  two"), ("b", "one two")])
    assert dedup_exact(df).count() == 1


def test_keeps_lowest_doc_id(spark):
    df = _prepared(spark, [("b", "same"), ("a", "same")])
    kept = [r.doc_id for r in dedup_exact(df).collect()]
    assert kept == ["a"]


def test_null_text_is_dropped(spark):
    df = _prepared(spark, [("a", None), ("b", None), ("c", "real text")])
    out = dedup_exact(df).collect()
    assert [r.doc_id for r in out] == ["c"]