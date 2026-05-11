from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.models.base import Base

class WisdomEntry(Base):
    __tablename__ = "daily_wisdoms"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wisdom_text: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    @property
    def title(self) -> str:
        """For compatibility with existing API, return wisdom_text as title"""
        return self.wisdom_text
    
    @property
    def description(self) -> str:
        """For compatibility with existing API, return wisdom_text as description"""
        return self.wisdom_text
    
    def __repr__(self):
        return f"WisdomEntry(id={self.id}, wisdom_text={self.wisdom_text[:50]}..., author={self.author})"
