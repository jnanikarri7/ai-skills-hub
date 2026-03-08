from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.interview import InterviewQ

router = APIRouter(prefix="/api/interview", tags=["interview"])

@router.get("", response_model=list[dict])
def list_questions(
    db: Session = Depends(get_db),
    difficulty: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=2000),
):
    qry = db.query(InterviewQ)
    if difficulty:
        qry = qry.filter(InterviewQ.difficulty == difficulty)
    questions = qry.order_by(InterviewQ.order_index, InterviewQ.id).limit(limit).all()
    return [
        {
            "id": q.id,
            "difficulty": q.difficulty,
            "question": q.question,
            "answer_html": q.answer_html,
            "code": q.code,
            "order_index": q.order_index,
        }
        for q in questions
    ]

@router.get("/{question_id}", response_model=dict)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(InterviewQ).filter(InterviewQ.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return {
        "id": q.id,
        "difficulty": q.difficulty,
        "question": q.question,
        "answer_html": q.answer_html,
        "code": q.code,
        "order_index": q.order_index,
    }