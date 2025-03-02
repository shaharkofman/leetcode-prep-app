from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from backend.database import Problem, SessionLocal

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#pydantic model for request/response body
class ProblemSchema(BaseModel):
    title: str
    difficulty: str
    url: str
    
    class Config:
        orm_mode = True
        
# Create a new problem
@app.post("/problems/", response_model=ProblemSchema)
def create_problem(problem: ProblemSchema, db: Session = Depends(get_db)):
    db_problem = Problem(**problem.dict())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

# Get all problems
@app.get("/problems/", response_model=List[ProblemSchema])
def get_problems(db: Session = Depends(get_db)):
    return db.query(Problem).all()

