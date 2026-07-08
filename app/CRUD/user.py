from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.schema.user import UserCreate#schema bata user create garna ko lagi request ma k k pathaune vanera define gareko ho
from app.model.user import User #model bata user ko table ko structure define gareko ho
from app.core.security import hash_password #security.py bata hash_password function import gareko ho, jasko kaam password lai hash garne ho

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    #check if user with the same email and username already exists in the database
    statement = select(User).where((User.email == user.email) | (User.username == user.username))
    result = await db.execute(statement)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the same email or username already exists."
        )
    
    
    hashed_password = hash_password(user.password)# hash_password function is called to hash the password provided by the user in the request. This is a security measure to ensure that the password is not stored in plain text in the database. The hashed password is then used when creating the new user record in the database.
    db_user = User(
        username=user.username,#schema bata pathaeko username lai model ma rakheko
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)#it tells the database session to add the new user object to the database
    await db.commit()#permanently save the changes made in the current transaction to the database
    await db.refresh(db_user)#refresh the db_user object with the latest data from the database, including any auto-generated fields like the primary key (id) and timestamps (created_at)
    return db_user