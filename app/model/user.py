from sqlalchemy import String, Integer, DateTime, func
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING: from app.model.task import Task  # to prevent circular import error,

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    owner: Mapped["Task"] = relationship("Task", back_populates="owner")  # Relationship to the Task model, allowing access to the tasks owned by the user