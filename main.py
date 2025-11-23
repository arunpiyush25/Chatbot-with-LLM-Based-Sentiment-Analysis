# main.py
"""
CLI entrypoint for the final system flow:
- rule-based chatbot handles conversation
- /end triggers Tier 2 (statement-level) and Tier 1 (Gemini) analyses
"""

from chatbot import SimpleChatbot
from utils import extract_user_messages
from sentiment_statement import analyze_statement
from sentiment_conversation import analyze_conversation_with_gemini
import os
import sys

LABEL_EMOJI = {"Positive": "🙂", "Negative": "😞", "Neutral": "😐"}

def print_separator():
    print("-" * 70)

def run_cli():
    bot = SimpleChatbot(name="LiaBot")
    print("LiaBot — Rule-based chatbot with sentiment analysis")
    print("Type messages. Commands: /end -> finish & analyze, /quit -> exit\n")

    while True:
        try:
            user = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            return

        if not user:
            continue

        if user.lower() == "/quit":
            print("Goodbye.")
            return

        if user.lower() == "/end":
            conv = bot.get_conversation_history()
            user_msgs = extract_user_messages(conv)

            # Tier 2 — Statement-level sentiment
            print_separator()
            print("Statement-level sentiment (Tier 2):")
            per_results = []
            for i, m in enumerate(user_msgs, 1):
                r = analyze_statement(m)
                per_results.append(r)
                emoji = LABEL_EMOJI.get(r["label"], "")
                print(f"{i:02d}. \"{r['text']}\" -> {r['label']} (score={r['score']:.3f}) {emoji}")

            # Build conversation text for Gemini (includes Bot messages to give context)
            conv_text = bot.as_text(include_bot=True)

            # Tier 1 — Conversation-level sentiment (Gemini)
            use_gemini = True
            # Allow override by env var to force local fallback
            if os.environ.get("FORCE_LOCAL_SENTIMENT", "").lower() in ("1", "true", "yes"):
                use_gemini = False

            try:
                llm_res = analyze_conversation_with_gemini(conv_text, use_gemini=use_gemini)
            except Exception as e:
                print_separator()
                print("Conversation-level sentiment: Failed to analyze with Gemini and fallback. Error:", e)
                return

            print_separator()
            print("Conversation-level sentiment (Tier 1):")
            print(f"Overall label: {llm_res['overall_label']} {LABEL_EMOJI.get(llm_res['overall_label'],'')}")
            print(f"Average score: {llm_res['average_score']:.3f}")
            print(f"Trend: {llm_res['trend']}")
            print(f"Confidence: {llm_res['confidence']:.2f}")
            print(f"Reason: {llm_res['reason']}")
            print_separator()
            return

        # normal message: bot handles it (rule-based)
        bot_reply = bot.handle_user(user)
        print(f"Bot: {bot_reply}")

if __name__ == "__main__":
    run_cli()
