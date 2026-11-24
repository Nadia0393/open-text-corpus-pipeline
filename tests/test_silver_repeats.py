from open_text_corpus_pipeline.silver.filters import (
    passes_repeated_ngrams,
    repeated_ngram_fraction,
)


def test_unique_prose_passes():
    text = "The quick brown fox jumps over the lazy dog near the river bank today"
    assert passes_repeated_ngrams(text) is True


def test_repeated_phrase_fails():
    assert passes_repeated_ngrams("buy now " * 20) is False


def test_repeated_fraction_is_one_for_pure_repetition():
    assert repeated_ngram_fraction("buy now " * 20) == 1.0


def test_short_text_has_no_repeats():
    assert repeated_ngram_fraction("one two") == 0.0
    assert passes_repeated_ngrams("one two") is True


def test_null_and_empty_text_fail():
    assert passes_repeated_ngrams(None) is False
    assert passes_repeated_ngrams("") is False