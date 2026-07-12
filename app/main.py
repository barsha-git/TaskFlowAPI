from fastapi import FastAPI
from app.router import auth
from app.router import task

app = FastAPI()
app.include_router(auth.router)#connect vayeko router lai FastAPI application sanga, so that the endpoints defined in the auth router can be accessed through the main application.
app.include_router(task.router)#connect vayeko router lai FastAPI application sanga, so that the endpoints defined in the task router can be accessed through the main application.