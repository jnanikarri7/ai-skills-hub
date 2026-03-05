from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillOut, SkillListOut

router = APIRouter(prefix="/api/skills", tags=["skills"])

def to_out(s: Skill) -> SkillOut:
    tags = [t.strip() for t in (s.tags_csv or "").split(",") if t.strip()]
    return SkillOut(
        slug=s.slug, name=s.name, category=s.category, level=s.level,
        is_trending=s.is_trending, estimated_hours=s.estimated_hours,
        short_summary=s.short_summary, why_important=s.why_important,
        example_snippet=s.example_snippet, practice_idea=s.practice_idea,
        tags=tags
    )

@router.get("", response_model=SkillListOut)
def list_skills(
    db: Session = Depends(get_db),
    category: str | None = Query(default=None),
    level: str | None = Query(default=None),
    trending: bool = Query(default=False),
    q: str | None = Query(default=None),
):
    qry = db.query(Skill)
    if category and category != "All":
        qry = qry.filter(Skill.category == category)
    if level and level != "All":
        qry = qry.filter(Skill.level == level)
    if trending:
        qry = qry.filter(Skill.is_trending.is_(True))
    if q:
        like = f"%{q}%"
        qry = qry.filter((Skill.name.ilike(like)) | (Skill.short_summary.ilike(like)))

    skills = qry.order_by(Skill.category, Skill.level, Skill.name).all()
    return SkillListOut(items=[to_out(s) for s in skills])

@router.get("/{slug}", response_model=SkillOut)
def get_skill(slug: str, db: Session = Depends(get_db)):
    s = db.query(Skill).filter(Skill.slug == slug).first()
    if not s:
        raise HTTPException(status_code=404, detail="Skill not found")
    return to_out(s)