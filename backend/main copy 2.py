from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import get_db, init_db
from semantic_search import find_best_answer
from learning import save_unknown_question, learn_from_feedback
from prediction import predict_answer

app = FastAPI(title="Stable MySQL Chatbot")

# CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
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

# Configuration
CONFIDENCE_THRESHOLD = 0.6

@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup"""
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint that finds answers or requests feedback for learning
    """
    message = payload.message.strip()
    
    if not message:
        return ChatResponse(
            answer="Please ask something.",
            needs_feedback=False,
            confidence=0.0
        )
    
    # Try to find best matching answer from knowledge base
    answer, score = find_best_answer(db, message)
    
    # If no good match found, use prediction and ask for feedback
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

@app.post("/feedback", response_model=FeedbackResponse)
def feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    """
    Feedback endpoint for learning new answers
    """
    result = learn_from_feedback(db, payload.question, payload.feedback)
    return FeedbackResponse(**result)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Serve frontend static files
try:
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
except Exception as e:
    print(f"Warning: Could not mount frontend directory: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
