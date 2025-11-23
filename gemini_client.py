# gemini_client.py
"""
Gemini client wrapper using the NEW google-genai SDK (v1.50+).
Uses the Client() class, not genai.configure().
"""

from typing import Dict, Any
import os
import json
import textwrap

try:
    from google.genai import Client
    _HAS_GENAI = True
except Exception:
    Client = None
    _HAS_GENAI = False

DEFAULT_MODEL = "gemini-2.0-flash"
MAX_PROMPT_CHARS = 20000

def _build_instruction():
    return textwrap.dedent("""\
    You are an assistant that analyzes the emotional direction of a conversation.
    Return output STRICTLY as JSON with the following keys:
      - overall_label: one of "Positive", "Negative", "Neutral"
      - average_score: a float in [-1.0, 1.0]
      - trend: one of "Improving", "Worsening", "Stable"
      - reason: short human-readable explanation
      - confidence: a float in [0, 1]
    Do NOT output anything except valid JSON.
    """)

def generate_json_from_conversation(conversation_text: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    if not _HAS_GENAI:
        raise RuntimeError("google-genai SDK not available.")

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set.")

    client = Client(api_key=api_key)

    instr = _build_instruction()
    if len(conversation_text) > MAX_PROMPT_CHARS:
        conversation_text = conversation_text[:MAX_PROMPT_CHARS] + "\n... [truncated]"

    prompt = f"{instr}\n\nconversation:\n{conversation_text}\n\nReturn ONLY the JSON."

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"temperature": 0.0, "max_output_tokens": 512}
    )

    output_text = response.text

    # Extract JSON
    start = output_text.find("{")
    end = output_text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise RuntimeError(f"Could not find JSON in Gemini output:\n{output_text}")

    json_text = output_text[start:end+1]
    parsed = json.loads(json_text)

    # Validate keys
    required = ["overall_label", "average_score", "trend", "reason", "confidence"]
    for r in required:
        if r not in parsed:
            raise RuntimeError(f"Missing key '{r}' in Gemini JSON: {parsed}")

    return parsed
