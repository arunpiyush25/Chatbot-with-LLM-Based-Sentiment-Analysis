# LiaPlus Chatbot with Sentiment Analysis

A modular chatbot system that performs both **statement-level** and **conversation-level** sentiment analysis.  
This project satisfies all **Tier 1 (mandatory)** and **Tier 2 (additional credit)** requirements of the assignment.

---

## Features

### Tier 1 – Conversation-Level Sentiment 
- Maintains complete conversation history.
- At `/end`, analyzes the **entire conversation**.
- Uses **Google Gemini** (via `google-genai`) to return:
  - overall sentiment label  
  - average sentiment score  
  - mood trend (Improving / Worsening / Stable)  
  - confidence  
  - short reasoning  

### Tier 2 – Statement-Level Sentiment 
- Analyzes **each user message individually**.
- Uses **DistilBERT transformer** sentiment model.
- Outputs label + numeric score for every message.
- Summarizes emotional trend across the conversation.

### Additional Enhancements
- Streamlit-based chat UI with message bubbles.
- Tier-1 sentiment shown in polished summary cards.
- Advanced rule-based chatbot with emotion-aware replies.
- Gemini fallback mode using local aggregation.
- Full testing with pytest.

---

## Project Structure
```
chatbot-sentiment/
│
├── chatbot.py
├── sentiment_statement.py
├── sentiment_conversation.py
├── gemini_client.py
├── utils.py
├── main.py
├── app.py
├── requirements.txt
├── README.md
└── tests/
├── test_statement.py
├── test_main_flow_local_fallback.py
└── test_conversation_gemini_mock.py
```

---

## How to Run

### 1. Create & activate virtual environment (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1 
```

### 2. Install dependencies
```powershell
pip install -r requirements.txt
```

### 3. Set Gemini API key
```powershell
Temporary: $env:GOOGLE_API_KEY="YOUR_KEY_HERE"
```

### 4. Run the terminal chatbot
```powershell
python main.py
```
Type /end to generate sentiment analysis.

### 5. Run the Streamlit UI (optional)
```powershell
streamlit run app.py
```
---

## Technologies Used

- Python 3.10+
- DistilBERT transformer (HuggingFace)
- Google Gemini via google-genai
- Streamlit
- Transformers
- Torch
- Pytest

---

## Sentiment Logic
### 1) Tier 2 – Per-Message Sentiment

- Implemented in sentiment_statement.py.
- Uses DistilBERT (distilbert-base-uncased-finetuned-sst-2-english).
- Converts model output into:
- Positive, Negative or Neutral
- Score is normalized to range [-1, 1].

### 2) Tier 1 – Conversation-Level Sentiment

- Implemented in sentiment_conversation.py.
- Sends full conversation to Gemini.
- Gemini returns JSON containing:
```powershell
{
  "overall_label": "Positive",
  "average_score": 0.61",
  "trend": "Improving",
  "reason": "...",
  "confidence": 0.91
}
```
If Gemini is unavailable, a fallback aggregator estimates sentiment based on individual messages.

---

## Status of Tier 2 Implementation

### Tier 2 is fully implemented, including:
- Per-message sentiment analysis.
- Sentiment scoring.
- Emotional trend summarization.
- Display in both terminal and Streamlit UI.

---

## Tests

Run all tests:
```powershell
pytest -q
```
Included tests:
- test_statement.py
- test_main_flow_local_fallback.py
- test_conversation_gemini_mock.py

All tests pass successfully.

---

## Enhancements & Innovations

- WhatsApp-style Streamlit chatbot interface.
- Automatic input clearing in UI.
- Beautiful card-based sentiment summary.
- Context-aware rule-based chatbot (not AI-generated).
- Gemini fallback sentiment logic.
- Clean, modular code structure suitable for production.

Example Interaction (Terminal)
```powershell
You: I am feeling sad today.
Bot: I'm really sorry you're going through that. Want to talk more?

You: But I met my friend later.
Bot: That's wonderful to hear! What made you feel that way?

You: /end
```

Statement-Level Output:
```powershell
01. I am feeling very sad
Sentiment: Negative
Score: -0.999
```

Conversation-Level Output:
```powershell
Overall Sentiment: Negative
Average Score: -0.7
Trend: Neutral
Confidence: 0.9
Reason: User expresses sadness, bot offers support, maintaining a negative but stable sentiment.
```
---

## 🧑‍💻 Author

**Piyush Arun [@arunpiyush25]**  
📍 M.Tech, Computer Science & Engineering — NIT Calicut  
🚀 Passionate about GenAI, Multi Agent systems, RAG, Langchain, Pinecone, Neo4j, LLMs, etc

---
