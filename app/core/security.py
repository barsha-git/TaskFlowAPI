from pwdlib import PasswordHash #pwdlib is a library for password hashing and verification. It provides a simple interface for securely hashing and verifying passwords using various algorithms. The PasswordHash class is used to create a password hasher object that can be used to hash and verify passwords.
from datetime import datetime, timezone, timedelta #datetime module is imported to work with date and time objects, which will be used to represent the created_at field in the UserResponse model. timezone is imported to work with time zones, and timedelta is imported to perform arithmetic operations on date and time objects, such as adding or subtracting time intervals. 
from jose import jwt #jose is a library for working with JSON Web Tokens (JWTs). It provides functions for encoding and decoding JWTs, as well as verifying their signatures. The jwt module is used to create and verify JWTs in the application.
from app.core.config import settings #settings.py bata settings import gareko ho, jasma database ko configuration haru define gareko ho


password_hasher = PasswordHash.recommended()#aafai recommend garcha jastai strong password(hash generate garna ko lagi)

def hash_password(password: str) -> str: #hash_password function is defined to hash a password using the pwdlib library. It takes a plain text password as input and returns the hashed version of the password.
    """Hash a password using pwdlib"""
    return password_hasher.hash(password)#password_hasher object ko hash method call garera password lai hash garne ho, ani hashed password return garne ho

def verify_password(password: str, hashed_password: str) -> bool:#verify_password function is defined to verify a password against a hashed password using the pwdlib library. It takes a plain text password and a hashed password as input and returns a boolean value indicating whether the password matches the hashed password.
    """Verify a password against a hashed password using pwdlib"""
    return password_hasher.verify(password, hashed_password)#password_hasher object ko verify method call garera password ra hashed_password lai compare garne ho, ani true or false return garne ho depending on whether the password matches the hashed password or not.

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:#create_access_token function is defined to create a JSON Web Token (JWT) for authentication purposes. It takes a dictionary of data to include in the token payload and an optional expiration time delta. It returns the encoded JWT as a string.
    """Create a JWT access token"""
    to_encode = data.copy()#data dictionary ko copy banau, jasma user ko information haru rakheko huncha, jasto ki user id, username, email, etc.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta#expires_delta parameter provide gareko cha vane, current UTC time ma expires_delta add garera token ko expiration time calculate garne ho
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)#expires_delta parameter provide nagareko cha vane, settings.py ma define gareko ACCESS_TOKEN_EXPIRE_MINUTES value use garera token ko expiration time calculate garne ho
    to_encode.update({"exp": expire})#to_encode dictionary ma "exp" key add garera expiration time set garne ho
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)#jwt.encode function call garera to_encode dictionary lai encode garne ho using the secret key and algorithm defined in settings.py. The result is the encoded JWT.
    return encoded_jwt#encoded JWT return garne ho
