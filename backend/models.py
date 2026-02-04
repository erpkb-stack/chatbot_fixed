from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, Float, Boolean, TIMESTAMP
from sqlalchemy.sql import func

Base = declarative_base()

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)

class UnknownQuestion(Base):
    __tablename__ = "unknown_questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    predicted_answer = Column(Text)
    user_feedback = Column(Text)
    confidence = Column(Float, default=0.0)
    resolved = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
