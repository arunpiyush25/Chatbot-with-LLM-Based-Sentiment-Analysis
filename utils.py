# utils.py
from typing import List, Tuple

def extract_user_messages(conversation: List[Tuple[str, str]]) -> List[str]:
    return [text for speaker, text in conversation if speaker == "User"]
