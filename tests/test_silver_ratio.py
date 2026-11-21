from open_text_corpus_pipeline.silver.filters import passes_non_alnum_ratio


def test_plain_prose_passes():
    assert passes_non_alnum_ratio("This is a normal sentence about history.") is True


def test_mostly_symbols_fails():
    assert passes_non_alnum_ratio("#!@*&^%$#!@*&^%$#!@") is False


def test_low_symbol_share_passes():
    # 2 symbols out of 10 non-space characters is well under 0.3
    assert passes_non_alnum_ratio("abcdefgh!!") is True


def test_high_symbol_share_fails():
    # 5 symbols out of 10 characters is above 0.3
    assert passes_non_alnum_ratio("abcde>>>>>") is False


def test_whitespace_is_not_counted_as_symbols():
    assert passes_non_alnum_ratio("a b c d e f g h") is True


def test_empty_and_null_text_fail():
    assert passes_non_alnum_ratio("") is False
    assert passes_non_alnum_ratio(None) is False