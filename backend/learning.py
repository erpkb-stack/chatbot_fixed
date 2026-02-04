from models import KnowledgeBase, UnknownQuestion

def save_unknown_question(db, question, predicted, confidence):
    """
    Save an unknown question to the database for future learning
    """
    if not question or not question.strip():
        return
    
    uq = UnknownQuestion(
        question=question,
        predicted_answer=predicted,
        confidence=confidence if confidence is not None else 0.0,
        resolved=False
    )
    db.add(uq)
    db.commit()

def learn_from_feedback(db, question, feedback):
    """
    Learn from user feedback by adding to knowledge base
    """
    if not question or not feedback:
        return {"status": "error", "message": "Question and feedback are required"}
    
    if len(feedback.strip()) < 3:
        return {"status": "error", "message": "Feedback is too short"}
    
    # Add to knowledge base
    kb = KnowledgeBase(
        question=question.strip(),
        answer=feedback.strip(),
        confidence=1.0
    )
    db.add(kb)
    
    # Mark unknown question as resolved
    db.query(UnknownQuestion).filter(
        UnknownQuestion.question == question,
        UnknownQuestion.resolved == False
    ).update({
        "user_feedback": feedback,
        "resolved": True
    })
    
    db.commit()
    return {"status": "success", "message": "Thank you! I've learned this."}
