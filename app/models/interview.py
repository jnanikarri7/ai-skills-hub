from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class InterviewQ(Base):
    __tablename__ = "interview_questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    difficulty: Mapped[str] = mapped_column(String(20), index=True)  # easy/medium/hard/system
    question: Mapped[str] = mapped_column(String(800))
    answer_html: Mapped[str] = mapped_column(Text)
    code: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)