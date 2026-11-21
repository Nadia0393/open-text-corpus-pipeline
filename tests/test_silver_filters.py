from open_text_corpus_pipeline.silver.filters import passes_length


def test_text_at_minimum_length_passes():
    assert passes_length("a" * 200) is True


def test_text_below_minimum_fails():
    assert passes_length("a" * 199) is False


def test_text_at_maximum_length_passes():
    assert passes_length("a" * 100_000) is True


def test_text_above_maximum_fails():
    assert passes_length("a" * 100_001) is False


def test_null_text_fails():
    assert passes_length(None) is False