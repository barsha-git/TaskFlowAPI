from fastapi import APIRouter, Depends, HTTPException#APIRouter is imported from FastAPI to create a router for handling authentication-related routes. Depends is imported to handle dependency injection, allowing the router to access the database session provided by the get_db function.
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm#OAuth2PasswordRequestForm is imported from FastAPI to handle the form data for user login requests, which includes the username and password fields.

from app.schema.user import TokenResponse, UserCreate, UserResponse, UserLogin, UserUpdate#schema bata user create garna ko lagi request ma k k pathaune vanera define gareko ho, ani response ma k k pathaune vanera define gareko ho
from app.CRUD.user import create_user, authenticate_user, update_user#CRUD bata create_user function import gareko ho, jasko kaam user lai database ma create garne ho
from app.dependency import get_db, get_current_user#dependency.py bata get_db function import gareko ho, jasko kaam database session provide garne ho
from app.core.security import create_access_token#security.py bata create_access_token function import gareko ho, jasko kaam JWT access token create garne ho

router = APIRouter(prefix="/auth", tags=["auth"])#prefix="/auth" means that all the routes defined in this router will be prefixed with "/auth", and tags=["auth"] is used for documentation purposes to group related endpoints together in the API documentation.
 
@router.post("/register", response_model=UserResponse) #register endpoint is defined to handle user registration requests. It accepts a POST request at the "/register" path and expects a UserCreate object in the request body. The response will be a UserResponse object, which includes the user's details after successful registration.
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):#register_user function is defined to handle the user registration process. It takes a UserCreate object as input, which contains the user's registration details, and an asynchronous database session (db) provided by the get_db dependency.
    db_user = await create_user(db, user)#database session (db) and user registration details (user) are passed to the create_user function, which handles the actual creation of the user in the database. The result is stored in the db_user variable.
    return db_user

#login endpoint is defined to handle user login requests. It accepts a POST request at the "/login" path and expects a UserLogin object in the request body. The response will be a dictionary containing the access token and token type.
@router.post("/Token", response_model=TokenResponse) 
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):#login_user function is defined to handle the user login process. It takes a UserLogin object as input, which contains the user's login credentials (username and password), and an asynchronous database session (db) provided by the get_db dependency.
    db_user = await authenticate_user(db, form_data.username, form_data.password)#database session (db), username, and password are passed to the authenticate_user function, which checks if the provided credentials match a user in the database. The result is stored in the db_user variable.
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")#If the authentication fails (i.e., db_user is None), an HTTPException is raised with a 401 status code and an error message indicating that the username or password is invalid.
    access_token = create_access_token(data={"sub": db_user.username})#If authentication is successful, the create_access_token function is called to generate a JWT access token. The user's username is included in the token payload under the "sub" key.
    return {"access_token": access_token, "token_type": "bearer"}#The function returns a dictionary containing the generated access token and the token type ("bearer"), which will be sent back to the client as the response to the login request.

#create a new endpoint to get the current user details based on the provided JWT token. It accepts a GET request at the "/me" path and returns a UserResponse object containing the user's details.
@router.get("/me", response_model=UserResponse)
async def get_current_user_details(current_user: UserResponse = Depends(get_current_user)):#get_current_user_details function is defined to retrieve the current user's details based on the provided JWT token. It takes a UserResponse object as input, which is obtained from the get_current_user dependency that validates the token and retrieves the corresponding user from the database.
    return current_user

#create a new endpoint to update the current user's details based on the provided JWT token. It accepts a PUT request at the "/me" path and expects a UserUpdate object in the request body. The response will be a UserResponse object containing the updated user's details.
@router.put("/me", response_model=UserResponse)
async def update_current_user_details(user_update: UserUpdate, current_user: UserResponse = Depends(get_current_user), db: AsyncSession = Depends(get_db)):#update_current_user_details function is defined to handle the user update process. It takes a UserUpdate object as input, which contains the user's updated details, a UserResponse object representing the current user obtained from the get_current_user dependency, and an asynchronous database session (db) provided by the get_db dependency.
    updated_user = await update_user(db, current_user, user_update)#database session (db), current user details (current_user), and updated user details (user_update) are passed to the update_user function, which handles the actual update of the user's information in the database. The result is stored in the updated_user variable.
    return updated_user