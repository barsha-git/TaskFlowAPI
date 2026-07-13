from sqlalchemy import String, Integer, DateTime, func, ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING 
if TYPE_CHECKING: from app.model.user import User #to prevent circualr import error, we use TYPE_CHECKING to conditionally import the User model only when type checking is performed. This allows us to reference the User model in the Task model without causing circular import issues during runtime.
from app.schema.enum import TaskStatus #importing the TaskStatus enum from the app.schema.enum module and aliasing it as T for use in the Task model. This allows us to define the status column in the Task model using the predefined enum values for task status.

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status: Mapped[TaskStatus] = mapped_column(String(20), nullable=False, default=TaskStatus.PENDING)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to the User table for task ownership
    owner: Mapped["User"] = relationship("User", back_populates="tasks")  # Relationship to the User model, allowing access to the user who owns the task