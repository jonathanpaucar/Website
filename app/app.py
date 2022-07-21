from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def welcome(db: Session=Depends(get_db)):
    x = crud.get_salary(db)
    return x
