# sentiment_statement.py
"""
Statement-level sentiment using transformers (DistilBERT fine-tuned for SST-2).
This is used for Tier 2: per-user-message sentiment analysis.

Outputs a dict:
{
  "text": str,
  "label": "Positive"|"Negative"|"Neutral",
  "score": float  # positive confidence for Positive, negative for Negative; for Neutral we map near 0
}

Implementation notes:
- Uses transformers pipeline("sentiment-analysis", model=...) with distilbert sst-2.
- Because SST-2 only returns POSITIVE/NEGATIVE, we convert low-confidence to NEUTRAL.
"""

from typing import Dict
from transformers import pipeline
import math

# Model choice: distilbert-base-uncased-finetuned-sst-2-english (small, accurate for sentences)
# The pipeline will download weight files on first run.
_PIPELINE = None

def get_pipeline():
    global _PIPELINE
    if _PIPELINE is None:
        _PIPELINE = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return _PIPELINE

def analyze_statement(text: str, neutral_threshold: float = 0.55) -> Dict:
    """
    Analyze single user statement.
    neutral_threshold: if classifier score < neutral_threshold -> treat as 'Neutral'
    Returns:
      {
        "text": text,
        "label": "Positive"/"Negative"/"Neutral",
        "score": float  # classifier confidence (0..1) for predicted class; if Neutral, score near 0
      }
    """
    text = (text or "").strip()
    if not text:
        return {"text": text, "label": "Neutral", "score": 0.0}

    pipe = get_pipeline()
    out = pipe(text, truncation=True, max_length=256)[0]  # {'label': 'POSITIVE', 'score': 0.999...}
    raw_label = out.get("label", "").upper()
    score = float(out.get("score", 0.0))

    if score < neutral_threshold:
        label = "Neutral"
        # Map score toward 0 for neutrality (signed mapping not necessary)
        mapped_score = 0.0
    else:
        label = "Positive" if raw_label.startswith("POS") else "Negative"
        # positive -> keep score, negative -> negative score
        mapped_score = score if label == "Positive" else -score

    return {"text": text, "label": label, "score": mapped_score}
