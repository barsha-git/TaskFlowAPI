from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.schema.user import UserCreate, UserLogin, UserUpdate#schema bata user create garna ko lagi request ma k k pathaune vanera define gareko ho
from app.model.user import User #model bata user ko table ko structure define gareko ho
from app.core.security import hash_password, verify_password #security.py bata hash_password function import gareko ho, jasko kaam password lai hash garne ho

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

#login ko lagi user lai database ma check garne function banau vani yo function use garne ho
async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None: #user verify garne, password verify garne, ani user return garne function banau vani yo function use garne ho
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    user = result.scalar_one_or_none() #scalar_one_or_none() method is called on the result of the query to retrieve a single user object from the database. If a user with the specified username exists, it will return that user object; otherwise, it will return None.
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):#verify_password function is called to check if the provided password matches the hashed password stored in the database for the user. If the passwords do not match, the function returns None, indicating that authentication failed.
        return None
    return user

#user update garna ko lagi
async def update_user(db: AsyncSession, user: User, user_update: UserUpdate) -> User:
    Update_dict = user_update.model_dump(exclude_unset=True)#model_dump() method is called on the user_update object to convert it into a dictionary. The exclude_unset=True argument ensures that only the fields that have been explicitly set in the user_update object are included in the resulting dictionary. This allows for partial updates, where only the provided fields are updated while leaving other fields unchanged.
    for key, value in Update_dict.items():#loop through the key-value pairs in the Update_dict dictionary. For each key-value pair, the corresponding attribute of the user object is updated with the new value.
        setattr(user, key, value)
    db.add(user)#it tells the database session to add the updated user object to the database
    await db.commit()#permanently save the changes made in the current transaction to the
    await db.refresh(user)#refresh the user object with the latest data from the database, including any auto-generated fields like the primary key (id) and timestamps (created_at)
    return user
                      