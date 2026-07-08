from pwdlib import PasswordHash #pwdlib is a library for password hashing and verification. It provides a simple interface for securely hashing and verifying passwords using various algorithms. The PasswordHash class is used to create a password hasher object that can be used to hash and verify passwords.

password_hasher = PasswordHash.recommended()#aafai recommend garcha jastai strong password(hash generate garna ko lagi)

def hash_password(password: str) -> str: #hash_password function is defined to hash a password using the pwdlib library. It takes a plain text password as input and returns the hashed version of the password.
    """Hash a password using pwdlib"""
    return password_hasher.hash(password)#password_hasher object ko hash method call garera password lai hash garne ho, ani hashed password return garne ho

def verify_password(password: str, hashed_password: str) -> bool:#verify_password function is defined to verify a password against a hashed password using the pwdlib library. It takes a plain text password and a hashed password as input and returns a boolean value indicating whether the password matches the hashed password.
    """Verify a password against a hashed password using pwdlib"""
    return password_hasher.verify(password, hashed_password)#password_hasher object ko verify method call garera password ra hashed_password lai compare garne ho, ani true or false return garne ho depending on whether the password matches the hashed password or not.