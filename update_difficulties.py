from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.interview import InterviewQ
import random

def update_difficulties():
    db: Session = SessionLocal()
    try:
        questions = db.query(InterviewQ).all()
        difficulties = ['easy', 'medium', 'hard', 'system']
        for q in questions:
            q.difficulty = random.choice(difficulties)
        db.commit()
        print(f"Updated difficulties for {len(questions)} questions.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_difficulties()