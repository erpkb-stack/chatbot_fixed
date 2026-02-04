from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models import KnowledgeBase

vectorizer = TfidfVectorizer()

def find_best_answer(db, user_question):
    """
    Find the best matching answer from knowledge base using TF-IDF and cosine similarity
    Returns: (answer, confidence_score)
    """
    rows = db.query(KnowledgeBase).all()
    
    if not rows:
        return None, 0.0
    
    if not user_question or not user_question.strip():
        return None, 0.0
    
    questions = [r.question for r in rows]
    
    try:
        # Fit vectorizer on all questions plus the user question
        vectors = vectorizer.fit_transform(questions + [user_question])
        
        # Calculate similarity between user question and all stored questions
        similarities = cosine_similarity(vectors[-1], vectors[:-1])[0]
        
        best_index = similarities.argmax()
        best_score = similarities[best_index]
        
        return rows[best_index].answer, float(best_score)
    except Exception as e:
        print(f"Error in semantic search: {e}")
        return None, 0.0
