from pydantic import BaseModel, EmailStr, ConfigDict#pydantic is a data validation and settings management library for Python. It provides a way to define data models using Python classes and type annotations. BaseModel is the base class for creating data models, EmailStr is a type that validates email addresses, and ConfigDict is used to configure model behavior.
from datetime import datetime#datetime module is imported to work with date and time objects, which will be used to represent the created_at field in the UserResponse model.

class UserCreate(BaseModel):#user create garna ko lagi request ma k k pathaune vanera define gareko ho
   
    username: str
    email: EmailStr
    password: str
    full_name: str | None = None

class UserResponse(BaseModel): #user lai pathauna ko lagi response ma k k pathaune vanera define gareko ho
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    created_at: datetime


#login ko lagi schema banau vani yo class use garne ho, ani response ma k k pathaune vanera define gareko ho
class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

#update garna ko lagi schema banau vani yo class use garne ho, ani response ma k k pathaune vanera define gareko ho
class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
