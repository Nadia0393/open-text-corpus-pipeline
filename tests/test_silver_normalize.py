from open_text_corpus_pipeline.silver.normalize import add_normalized_text, normalize_text


def test_nfc_composes_combining_characters():
    decomposed = "cafe\u0301"          # "e" followed by a combining accent
    assert normalize_text(decomposed) == "caf\u00e9"


def test_crlf_and_cr_become_lf():
    assert normalize_text("a\r\nb\rc") == "a\nb\nc"


def test_inner_spaces_collapse_and_lines_strip():
    assert normalize_text("  one   two \t three  \n  four ") == "one two three\nfour"


def test_long_blank_runs_collapse_to_one_paragraph_break():
    assert normalize_text("a\n\n\n\n\nb") == "a\n\nb"


def test_normalization_is_idempotent():
    once = normalize_text("  messy\r\n\r\n\r\n\r\ntext\u00a0here  ")
    assert normalize_text(once) == once


def test_null_stays_null():
    assert normalize_text(None) is None


def test_spark_column_keeps_raw_text_and_row_count(spark):
    df = spark.createDataFrame(
        [("1", "  a  b  "), ("2", None)],
        ["source_id", "text"],
    )
    out = add_normalized_text(df).orderBy("source_id").collect()
    assert len(out) == 2
    assert out[0].text == "  a  b  "
    assert out[0].text_normalized == "a b"
    assert out[1].text_normalized is None