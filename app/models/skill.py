from sqlalchemy import String, Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    category: Mapped[str] = mapped_column(String(40), index=True)       # Foundations/ML/MLOps/LLM/Streaming/DQ
    level: Mapped[str] = mapped_column(String(20), index=True)          # Beginner/Intermediate/Advanced
    is_trending: Mapped[bool] = mapped_column(Boolean, default=False)
    estimated_hours: Mapped[int] = mapped_column(Integer, default=6)

    short_summary: Mapped[str] = mapped_column(String(500))
    why_important: Mapped[str] = mapped_column(String(800))
    example_snippet: Mapped[str] = mapped_column(Text)
    practice_idea: Mapped[str] = mapped_column(String(800))
    tags_csv: Mapped[str] = mapped_column(String(500), default="")      # "spark,pyspark,big data"