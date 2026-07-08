from fastapi import APIRouter, Depends#APIRouter is imported from FastAPI to create a router for handling authentication-related routes. Depends is imported to handle dependency injection, allowing the router to access the database session provided by the get_db function.
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.user import UserCreate, UserResponse#schema bata user create garna ko lagi request ma k k pathaune vanera define gareko ho, ani response ma k k pathaune vanera define gareko ho
from app.CRUD.user import create_user#CRUD bata create_user function import gareko ho, jasko kaam user lai database ma create garne ho
from app.dependency import get_db#dependency.py bata get_db function import gareko ho, jasko kaam database session provide garne ho

router = APIRouter(prefix="/auth", tags=["auth"])#prefix="/auth" means that all the routes defined in this router will be prefixed with "/auth", and tags=["auth"] is used for documentation purposes to group related endpoints together in the API documentation.
 
@router.post("/register", response_model=UserResponse) #register endpoint is defined to handle user registration requests. It accepts a POST request at the "/register" path and expects a UserCreate object in the request body. The response will be a UserResponse object, which includes the user's details after successful registration.
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):#register_user function is defined to handle the user registration process. It takes a UserCreate object as input, which contains the user's registration details, and an asynchronous database session (db) provided by the get_db dependency.
    db_user = await create_user(db, user)#database session (db) and user registration details (user) are passed to the create_user function, which handles the actual creation of the user in the database. The result is stored in the db_user variable.
    return db_user