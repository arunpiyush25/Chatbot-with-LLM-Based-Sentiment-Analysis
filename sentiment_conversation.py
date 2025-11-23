# sentiment_conversation.py
"""
Wrapper for conversation-level sentiment.
- Primary flow: call gemini_client.generate_json_from_conversation
- Fallback: simple aggregator (averaging statement-level scores) if Gemini not available or forced offline.
"""

from typing import Dict, Any
import logging

from gemini_client import generate_json_from_conversation, DEFAULT_MODEL
from sentiment_statement import analyze_statement

logger = logging.getLogger(__name__)

def analyze_conversation_with_gemini(conversation_text: str, model: str = DEFAULT_MODEL, use_gemini: bool = True) -> Dict[str, Any]:
    """
    Returns dict with keys:
    - overall_label
    - average_score
    - trend
    - reason
    - confidence
    If use_gemini is False or gemini fails, falls back to _fallback_aggregate.
    """
    if use_gemini:
        try:
            return generate_json_from_conversation(conversation_text, model=model)
        except Exception as e:
            logger.warning("Gemini call failed, falling back to local aggregation: %s", e)

    # fallback
    return _fallback_aggregate_from_text(conversation_text)

def _fallback_aggregate_from_text(conv_text: str) -> Dict[str, Any]:
    """
    Very simple fallback: parse lines that start with 'User:' and analyze them
    with statement-level sentiment. Compute average_score and trend heuristic.
    """
    lines = [l.strip() for l in conv_text.splitlines() if l.strip()]
    user_texts = []
    for l in lines:
        if l.startswith("User:"):
            user_texts.append(l[len("User:"):].strip())
    if not user_texts:
        return {
            "overall_label": "Neutral",
            "average_score": 0.0,
            "trend": "Stable",
            "reason": "No user messages found in conversation.",
            "confidence": 0.25
        }
    per = [analyze_statement(t) for t in user_texts]
    scores = [p["score"] for p in per]
    avg = sum(scores) / len(scores)
    # label mapping
    if avg >= 0.05:
        label = "Positive"
    elif avg <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    # trend: compare first vs last half
    n = len(scores)
    half = max(1, n // 2)
    first_avg = sum(scores[:half]) / half
    last_avg = sum(scores[-half:]) / half
    delta = last_avg - first_avg
    if delta >= 0.05:
        trend = "Improving"
    elif delta <= -0.05:
        trend = "Worsening"
    else:
        trend = "Stable"

    reason = f"Aggregated {len(scores)} user messages; avg score {avg:.3f}."
    confidence = min(0.8, 0.4 + abs(avg) * 0.6)  # heuristic
    return {"overall_label": label, "average_score": float(avg), "trend": trend, "reason": reason, "confidence": float(confidence)}
