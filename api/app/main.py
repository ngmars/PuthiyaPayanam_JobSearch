from fastapi import FastAPI
from .database import Base, engine
from .auth.router import router as auth_router
from .user.router import router as user_router
Base.metadata.create_all(bind=engine)

app = FastAPI()
# Include Routers
app.include_router(auth_router) # Authentication Router
app.include_router(user_router) # User Route
@app.get("/")

def root():
    return({
        "message":"FASTAPI for JOBme is running"
    })