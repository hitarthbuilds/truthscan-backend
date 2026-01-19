# TruthScan Backend

TruthScan is an AI-powered credibility analysis backend that evaluates **text claims and images** to surface **risk signals**, not absolute truth.

This service exposes a REST API built with **FastAPI**, designed to be consumed by a frontend (Streamlit, web, or mobile).

---

## 🚀 Features

- Text claim verification with confidence scoring
- Image verification with manipulation risk detection
- Unified risk scoring engine
- Rate-limited API endpoints
- Production-ready FastAPI architecture

---

## 🧠 What This Backend Does (Conceptually)

TruthScan does **risk assessment**, not fact-checking.

For each input:
- The model estimates **confidence**
- Heuristics + signals produce a **risk score**
- The system explains *why* something was flagged

This makes it suitable for:
- Misinformation detection
- Pre-screening content
- Human-in-the-loop moderation tools

---

## 🛠️ Tech Stack

- **FastAPI** – API framework
- **Uvicorn** – ASGI server
- **Pydantic** – data validation
- **SlowAPI** – rate limiting
- **Pillow (PIL)** – image handling
- **Transformers (lightweight usage)** – text analysis utilities

---

## 📡 API Endpoints

### Verify Text Claim

POST /verify/text

**Request**
```json
{
  "text": "the sun is going to explode tomorrow"
}

Response

{
  "verdict": "Unlikely but low risk",
  "confidence": 0.75,
  "risk_score": 0.24,
  "flags": ["temporal_improbability"]
}

Verify Image

POST /verify/image

Form Data
	•	image: JPG / PNG file

Response

{
  "verdict": "Potentially manipulated",
  "confidence": 0.60,
  "risk_score": 0.70,
  "image_flags": ["missing_metadata", "screenshot_like"]
}

⚙️ Local Development

git clone https://github.com/your-username/truthscan-backend.git
cd truthscan-backend
pip install -r requirements.txt
uvicorn app.main:app --reload

Server runs at:

http://127.0.0.1:8000

🌍 Deployment
	•	Deployed on Railway
	•	Dockerized backend
	•	Public API endpoint exposed for frontend consumption

⸻

⚠️ Disclaimer

TruthScan does not determine truth.
It highlights risk indicators to support critical thinking.


📄 License

MIT License

