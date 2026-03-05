from pydantic import BaseModel

class SkillOut(BaseModel):
    slug: str
    name: str
    category: str
    level: str
    is_trending: bool
    estimated_hours: int
    short_summary: str
    why_important: str
    example_snippet: str
    practice_idea: str
    tags: list[str]

class SkillListOut(BaseModel):
    items: list[SkillOut]