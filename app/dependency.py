from app.core.database import SessionLocal#core/database.py bata SessionLocal import gareko ho, jasko kaam database session create garne ho
from fastapi.security import OAuth2PasswordBearer#fastapi.security bata OAuth2PasswordBearer import gareko ho, jasko kaam authentication ko lagi token-based authentication handle garne ho

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")#OAuth2PasswordBearer
from jose import JWTError, jwt#jose library bata JWTError and jwt import gareko ho, jasko kaam JSON Web Token (JWT) handle garne ho
from fastapi import Depends, HTTPException, status#fastapi bata Depends, HTTPException, status import gareko ho, jasko kaam dependency injection, error handling, and HTTP status codes handle garne ho
from sqlalchemy import select#sqlalchemy bata select import gareko ho, jasko kaam database query banau ko lagi ho
from app.model.user import User#model bata user ko table ko structure define gareko ho

from app.core.config import settings#core/config.py bata settings import gareko ho, jasko kaam application ko configuration settings handle garne ho
from sqlalchemy.ext.asyncio import AsyncSession#sQLAlchemy ko AsyncSession import gareko ho, jasko kaam asynchronous database session handle garne ho
from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:#database session generator function that yields an asynchronous database session for use in FastAPI endpoints
    async with SessionLocal() as session:#SessionLocal() is called to create a new asynchronous database session. The async with statement ensures that the session is properly closed after use, even if an error occurs during the execution of the code block.
        yield session 

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):#get_current_user function is defined to retrieve the current user based on the provided JWT token. It takes a token as input, which is obtained from the request's Authorization header using the oauth2_scheme dependency.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )#credentials_exception variable is defined to create an HTTPException that will be raised if the token validation fails. It includes a 401 status code, an error message, and a WWW-Authenticate header indicating that the request requires Bearer authentication.

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])#jwt.decode function is called to decode the provided JWT token using the secret key and algorithm defined in the settings. If the token is valid, the payload (the data contained in the token) is extracted.
        username: str = payload.get("sub")#The username is extracted from the payload using the "sub" key. If the "sub" key is not present in the payload, username will be None.
        if username is None:
            raise credentials_exception#If the username is None (i.e., the "sub" key was not found in the payload), the credentials_exception is raised, indicating that the token validation failed.
    except JWTError:
        raise credentials_exception#If any JWTError occurs during the decoding process (e.g., invalid token, expired token), the credentials_exception is raised.

    statement = select(User).where(User.username == username)#A SQLAlchemy select statement is created to query the User table for a user with the specified username.
    result = await db.execute(statement)#The select statement is executed asynchronously using the provided database session (db).
    user = result.scalar_one_or_none()#The scalar_one_or_none() method is called on the result of the query to retrieve a single user object from the database. If a user with the specified username exists, it will return that user object; otherwise, it will return None.

    if user is None:
        raise credentials_exception#If no user was found in the database (i.e., user is None), the credentials_exception is raised, indicating that the token validation failed.

    return user#If a valid user was found, it is returned as the result of the get_current_user function.


