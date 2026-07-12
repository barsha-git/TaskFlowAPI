from pydantic import BaseModel, ConfigDict  # pydantic is a data validation and settings management library for Python. It provides a way to define data models using Python classes and type annotations. BaseModel is the base class for creating data models, EmailStr is a type that validates email addresses, and ConfigDict is used to configure model behavior.
from datetime import datetime  # datetime module is imported to work with date and time objects, which will be used to represent the created_at field in the UserResponse model.

class TaskCreate(BaseModel):  # user create garna ko lagi request ma k k pathaune vanera define gareko ho
    title: str
    description: str | None = None
    status: str | None = "pending"  # Default status is set to "pending" if not provided

class TaskResponse(BaseModel):  # user lai pathauna ko lagi response ma k k pathaune vanera define gareko ho
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    status: str
    owner_id: int

class TaskUpdate(BaseModel):  # update garna ko lagi schema banau vani yo class use garne ho, ani response ma k k pathaune vanera define gareko ho
    title: str | None = None
    description: str | None = None
    status: str | None = None

