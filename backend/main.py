from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from db import get_db, init_db
from semantic_search import find_best_answer
from learning import save_unknown_question, learn_from_feedback
from prediction import predict_answer

app = FastAPI(title="Stable MySQL Chatbot")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Models ----------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    needs_feedback: bool = False
    confidence: float = 0.0

class FeedbackRequest(BaseModel):
    question: str
    feedback: str

class FeedbackResponse(BaseModel):
    status: str
    message: str = ""

CONFIDENCE_THRESHOLD = 0.6

# ---------------- Startup ----------------
@app.on_event("startup")
def startup_event():
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

# ---------------- Chat API ----------------
@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    message = payload.message.strip()

    if not message:
        return ChatResponse(
            answer="Please ask something.",
            needs_feedback=False,
            confidence=0.0
        )

    answer, score = find_best_answer(db, message)

    if not answer or score < CONFIDENCE_THRESHOLD:
        predicted = predict_answer(message)
        save_unknown_question(db, message, predicted, score)
        return ChatResponse(
            answer=predicted,
            needs_feedback=True,
            confidence=score
        )

    return ChatResponse(
        answer=answer,
        needs_feedback=False,
        confidence=score
    )

# ---------------- Feedback API ----------------
@app.post("/feedback", response_model=FeedbackResponse)
def feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    result = learn_from_feedback(db, payload.question, payload.feedback)
    return FeedbackResponse(**result)

# ---------------- Health ----------------
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ---------------- Frontend Mount ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_path = os.path.join(BASE_DIR, "frontend")

try:
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    print(f"Frontend mounted from: {frontend_path}")
except Exception as e:
    print(f"Warning: Could not mount frontend directory: {e}")

# ---------------- Run ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
