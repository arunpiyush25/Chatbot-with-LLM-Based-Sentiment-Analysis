# chatbot.py
"""
Advanced rule-based chatbot. No AI.
Provides varied, context-aware responses.
Stores full conversation history.
"""

from typing import List, Tuple
import re
import random

class SimpleChatbot:
    def __init__(self, name: str = "LiaBot"):
        self.name = name
        self.conversation: List[Tuple[str, str]] = []

        # Predefined response sets (variety to avoid repetition)
        self.greeting_responses = [
            "Hi! How are you feeling today?",
            "Hello! What’s on your mind?",
            "Hey there! How can I help you today?",
        ]

        self.positive_responses = [
            "That's wonderful to hear! What made you feel that way?",
            "I'm glad to hear something positive happened. Want to share more?",
            "Sounds great! Tell me more about the good part.",
        ]

        self.negative_responses = [
            "I'm really sorry you're going through that. Want to talk more?",
            "That sounds tough… I'm here to listen.",
            "I'm sorry you feel this way. What do you think caused it?",
        ]

        self.neutral_responses = [
            "I get you. Would you like to explain a bit more?",
            "Interesting—tell me more so I can understand better.",
            "Okay, I’m listening. What else happened?",
        ]

        self.followup_questions = [
            "What happened next?",
            "How did that make you feel overall?",
            "Do you want to talk more about it?",
            "I'm listening — go on.",
        ]

    # ----------------------------
    # Conversation storage helpers
    # ----------------------------
    def add_user_message(self, text: str):
        self.conversation.append(("User", text.strip()))

    def add_bot_message(self, text: str):
        self.conversation.append(("Bot", text.strip()))

    def get_conversation_history(self) -> List[Tuple[str, str]]:
        return list(self.conversation)

    def get_user_messages(self) -> List[str]:
        return [t for s, t in self.conversation if s == "User"]

    def as_text(self, include_bot: bool = True) -> str:
        lines = []
        for speaker, text in self.conversation:
            if not include_bot and speaker == "Bot":
                continue
            lines.append(f"{speaker}: {text}")
        return "\n".join(lines)

    def last_user_message(self) -> str:
        for s, t in reversed(self.conversation):
            if s == "User":
                return t
        return ""

    # ----------------------------
    # Core rule-based logic
    # ----------------------------
    def simple_response(self, user_text: str) -> str:
        txt = user_text.strip()
        l = txt.lower()

        # 1. Greetings
        if re.search(r"\b(hi|hello|hey|good morning|good evening)\b", l):
            return random.choice(self.greeting_responses)

        # 2. Thanks
        if re.search(r"\b(thank(s| you)?|thx|ty)\b", l):
            return "You're welcome! I’m glad I could help."

        # 3. Goodbyes
        if re.search(r"\b(bye|goodbye|see you|farewell)\b", l):
            return "Goodbye! If you'd like to talk again, I’ll be here."

        # 4. Strong positive emotions
        if re.search(r"\b(happy|excited|great|awesome|good|glad|amazing)\b", l):
            return random.choice(self.positive_responses)

        # 5. Strong negative emotions
        if re.search(r"\b(sad|upset|angry|hurt|frustrat|bad|terrible|depress)\b", l):
            return random.choice(self.negative_responses)

        # 6. Direct questions
        if "?" in txt or re.search(r"\b(how|what|why|when|where|can you|could you|should I)\b", l):
            return (
                "That's an interesting question. "
                "Could you tell me more so I can understand the situation better?"
            )

        # 7. Very short messages
        if len(txt.split()) <= 2:
            return f"I hear you: '{txt}'. Could you explain a bit more?"

        # 8. Neutral descriptive statements
        return random.choice(self.neutral_responses) + " " + random.choice(self.followup_questions)

    # ----------------------------
    # Handle message
    # ----------------------------
    def handle_user(self, text: str) -> str:
        self.add_user_message(text)
        reply = self.simple_response(text)
        self.add_bot_message(reply)
        return reply
