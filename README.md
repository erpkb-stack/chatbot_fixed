# Stable MySQL AI Chatbot

An intelligent chatbot that learns from user feedback using MySQL, FastAPI, and machine learning.

## Features

- **Semantic Search**: Uses TF-IDF and cosine similarity to find best matching answers
- **Auto-Learning**: Learns from user feedback when it doesn't know an answer
- **Confidence Scoring**: Shows confidence level for each response
- **Modern UI**: Clean, responsive web interface
- **REST API**: FastAPI backend with proper validation

## Fixed Issues

### Backend Fixes:
1. ✅ Added missing `scikit-learn` dependency to requirements.txt
2. ✅ Added `pydantic` for request/response validation
3. ✅ Fixed import statements (removed `backend.` prefix for cleaner imports)
4. ✅ Added CORS middleware for frontend-backend communication
5. ✅ Added database initialization function (`init_db()`)
6. ✅ Added Pydantic models for type safety
7. ✅ Added better error handling and validation
8. ✅ Added health check endpoint
9. ✅ Fixed model definitions with proper nullable constraints
10. ✅ Added startup event to auto-create database tables

### Frontend Fixes:
1. ✅ Improved UI with modern, responsive design
2. ✅ Added error handling for API calls
3. ✅ Added loading states and animations
4. ✅ Added Enter key support for sending messages
5. ✅ Added confidence display
6. ✅ Better feedback form UX
7. ✅ Added welcome message

## Prerequisites

- Python 3.8+
- MySQL Server running on localhost:3306
- MySQL database named `chatbot_ai`
- MySQL user `root` with password `rootroot`

## Setup Instructions

### 1. Create MySQL Database

```sql
CREATE DATABASE chatbot_ai;
```

### 2. Install Dependencies

```bash
# Navigate to project directory
cd chatbot_fixed

# Install Python packages
pip install -r requirements.txt
```

### 3. Run the Application

```bash
# Start from the backend directory
cd backend
python main.py
```

The application will:
- Automatically create database tables on startup
- Start the server on `http://localhost:8000`
- Serve the frontend at `http://localhost:8000`

### 4. Access the Chatbot

Open your browser and navigate to:
```
http://localhost:8000
```

## Project Structure

```
chatbot_fixed/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with CORS and endpoints
│   ├── db.py                # Database connection and initialization
│   ├── models.py            # SQLAlchemy ORM models
│   ├── semantic_search.py   # TF-IDF similarity search
│   ├── prediction.py        # Answer prediction logic
│   └── learning.py          # Learning from feedback
├── frontend/
│   ├── index.html           # Modern UI
│   └── app.js               # Frontend logic
└── requirements.txt         # Python dependencies
```

## How It Works

1. **User asks a question**: The chatbot searches its knowledge base using semantic similarity
2. **High confidence match**: Returns the answer immediately
3. **Low confidence**: Shows a prediction and asks for user feedback
4. **User provides feedback**: The chatbot learns and stores the correct answer
5. **Future questions**: The chatbot can now answer similar questions confidently

## Database Schema

### knowledge_base
- `id`: Primary key
- `question`: Question text
- `answer`: Answer text  
- `confidence`: Confidence score (0.0 to 1.0)

### unknown_questions
- `id`: Primary key
- `question`: Question that wasn't answered confidently
- `predicted_answer`: Bot's prediction
- `user_feedback`: Correct answer from user
- `confidence`: Original confidence score
- `resolved`: Whether feedback was provided
- `created_at`: Timestamp

## Configuration

Edit these values in `backend/db.py`:

```python
DATABASE_URL = "mysql+pymysql://root:rootroot@localhost:3306/chatbot_ai"
```

Edit confidence threshold in `backend/main.py`:

```python
CONFIDENCE_THRESHOLD = 0.6  # Adjust between 0.0 and 1.0
```

## API Endpoints

### POST /chat
Request:
```json
{
  "message": "What is Python?"
}
```

Response:
```json
{
  "answer": "Python is a programming language...",
  "needs_feedback": false,
  "confidence": 0.85
}
```

### POST /feedback
Request:
```json
{
  "question": "What is Python?",
  "feedback": "Python is a high-level programming language..."
}
```

Response:
```json
{
  "status": "success",
  "message": "Thank you! I've learned this."
}
```

### GET /health
Response:
```json
{
  "status": "healthy"
}
```

## Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Check database credentials in `db.py`
- Verify database `chatbot_ai` exists

### Import Errors
- Make sure you're running from the `backend/` directory
- Verify all dependencies are installed: `pip install -r requirements.txt`

### CORS Issues
- The app includes CORS middleware
- For production, update `allow_origins` in `main.py`

### Frontend Can't Connect
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify frontend files are in `frontend/` directory

## Future Enhancements

- Add user authentication
- Implement more sophisticated ML models for prediction
- Add conversation history
- Support for multiple languages
- Add analytics dashboard
- Export/import knowledge base
- Batch learning from CSV files

## License

MIT License
# chatbot_fixed
