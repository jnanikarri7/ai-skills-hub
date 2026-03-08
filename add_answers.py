from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.interview import InterviewQ
import random

def add_dummy_answers():
    db: Session = SessionLocal()
    try:
        questions = db.query(InterviewQ).filter(InterviewQ.answer_html == '').all()
        dummy_answers = [
            "This is a key concept in data engineering. Focus on understanding the core principles and practical applications.",
            "In data engineering interviews, demonstrate your knowledge of system design and trade-offs.",
            "Practice explaining technical concepts clearly. Use examples from real-world scenarios.",
            "Master the fundamentals before diving into advanced topics. Build strong foundations.",
            "Consider scalability, reliability, and maintainability when designing solutions.",
            "Think about data flow, processing pipelines, and optimization strategies.",
            "Understand the differences between various technologies and when to use each.",
            "Focus on problem-solving approaches and algorithmic thinking.",
            "Learn from case studies and real-world implementations.",
            "Practice explaining complex topics in simple terms."
        ]
        for q in questions:
            q.answer_html = random.choice(dummy_answers)
        db.commit()
        print(f"Added dummy answers to {len(questions)} questions.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_dummy_answers()