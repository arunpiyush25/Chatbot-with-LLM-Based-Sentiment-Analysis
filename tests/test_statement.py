import pytest
from sentiment_statement import analyze_statement

def test_statement_positive():
    r = analyze_statement("I love this product!", neutral_threshold=0.5)
    assert "label" in r
    assert r["label"] in ("Positive", "Neutral", "Negative")
    # confident positive should be Positive
    assert r["label"] == "Positive"

def test_statement_neutral_empty():
    r = analyze_statement("", neutral_threshold=0.5)
    assert r["label"] == "Neutral"
    assert r["score"] == 0.0
