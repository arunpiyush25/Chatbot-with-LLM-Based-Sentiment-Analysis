# tests/test_conversation_gemini_mock.py

import pytest
import sentiment_conversation

def fake_gen_json(conv_text, model=""):
    return {
        "overall_label": "Negative",
        "average_score": -0.22,
        "trend": "Improving",
        "reason": "Conversation started negative but improved.",
        "confidence": 0.91
    }

def test_conversation_with_mock(monkeypatch):
    # PATCH THE LOCAL REFERENCE inside sentiment_conversation
    monkeypatch.setattr(
        sentiment_conversation,
        "generate_json_from_conversation",
        fake_gen_json
    )

    conv_text = "User: I'm upset.\nBot: I'm sorry to hear.\nUser: It got better later."

    # Force Gemini path (mock will be used)
    res = sentiment_conversation.analyze_conversation_with_gemini(
        conv_text,
        use_gemini=True
    )

    assert res["overall_label"] == "Negative"
    assert res["trend"] == "Improving"
    assert res["confidence"] == 0.91
