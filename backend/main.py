from fastapi import FastAPI
from .database import Problem, SessionLocal

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}
