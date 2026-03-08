from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.progress import SkillProgress
from app.api.routes_auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.get("", response_model=list[dict])
def get_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    progresses = db.query(SkillProgress).filter(SkillProgress.user_id == current_user.id).all()
    return [
        {
            "skill_slug": p.skill_slug,
            "completed": p.completed,
            "hours_logged": p.hours_logged,
            "updated_at": p.updated_at,
        }
        for p in progresses
    ]

@router.post("/{skill_slug}")
def update_progress(skill_slug: str, completed: bool = None, hours_logged: int = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    progress = db.query(SkillProgress).filter(SkillProgress.user_id == current_user.id, SkillProgress.skill_slug == skill_slug).first()
    if not progress:
        progress = SkillProgress(user_id=current_user.id, skill_slug=skill_slug)
        db.add(progress)
    if completed is not None:
        progress.completed = completed
    if hours_logged is not None:
        progress.hours_logged = hours_logged
    db.commit()
    return {"message": "Progress updated"}