# tests/test_main_flow_local_fallback.py
from chatbot import SimpleChatbot
from sentiment_conversation import _fallback_aggregate_from_text

def test_fallback_aggregation_simple():
    bot = SimpleChatbot()
    bot.handle_user("I hate this")
    bot.handle_user("Actually it improved")
    conv_text = bot.as_text(include_bot=True)
    res = _fallback_aggregate_from_text(conv_text)
    assert "overall_label" in res
    assert "average_score" in res
    assert "trend" in res
