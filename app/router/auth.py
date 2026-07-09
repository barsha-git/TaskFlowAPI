from fastapi import APIRouter, Depends, HTTPException#APIRouter is imported from FastAPI to create a router for handling authentication-related routes. Depends is imported to handle dependency injection, allowing the router to access the database session provided by the get_db function.
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.user import TokenResponse, UserCreate, UserResponse, UserLogin#schema bata user create garna ko lagi request ma k k pathaune vanera define gareko ho, ani response ma k k pathaune vanera define gareko ho
from app.CRUD.user import create_user, authenticate_user#CRUD bata create_user function import gareko ho, jasko kaam user lai database ma create garne ho
from app.dependency import get_db#dependency.py bata get_db function import gareko ho, jasko kaam database session provide garne ho
from app.core.security import create_access_token#security.py bata create_access_token function import gareko ho, jasko kaam JWT access token create garne ho

router = APIRouter(prefix="/auth", tags=["auth"])#prefix="/auth" means that all the routes defined in this router will be prefixed with "/auth", and tags=["auth"] is used for documentation purposes to group related endpoints together in the API documentation.
 
@router.post("/register", response_model=UserResponse) #register endpoint is defined to handle user registration requests. It accepts a POST request at the "/register" path and expects a UserCreate object in the request body. The response will be a UserResponse object, which includes the user's details after successful registration.
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):#register_user function is defined to handle the user registration process. It takes a UserCreate object as input, which contains the user's registration details, and an asynchronous database session (db) provided by the get_db dependency.
    db_user = await create_user(db, user)#database session (db) and user registration details (user) are passed to the create_user function, which handles the actual creation of the user in the database. The result is stored in the db_user variable.
    return db_user

#login endpoint is defined to handle user login requests. It accepts a POST request at the "/login" path and expects a UserLogin object in the request body. The response will be a dictionary containing the access token and token type.
@router.post("/Token", response_model=TokenResponse) 
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):#login_user function is defined to handle the user login process. It takes a UserLogin object as input, which contains the user's login credentials (username and password), and an asynchronous database session (db) provided by the get_db dependency.
    db_user = await authenticate_user(db, user.username, user.password)#database session (db), username, and password are passed to the authenticate_user function, which checks if the provided credentials match a user in the database. The result is stored in the db_user variable.
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")#If the authentication fails (i.e., db_user is None), an HTTPException is raised with a 401 status code and an error message indicating that the username or password is invalid.
    access_token = create_access_token(data={"sub": db_user.username})#If authentication is successful, the create_access_token function is called to generate a JWT access token. The user's username is included in the token payload under the "sub" key.
    return {"access_token": access_token, "token_type": "bearer"}#The function returns a dictionary containing the generated access token and the token type ("bearer"), which will be sent back to the client as the response to the login request.