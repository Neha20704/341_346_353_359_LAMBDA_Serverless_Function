from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/functions", response_model=schemas.FunctionOut)
def create(function: schemas.FunctionCreate, db: Session = Depends(get_db)):
    return crud.create_function(db, function)

@app.get("/functions", response_model=list[schemas.FunctionOut])
def read_all(db: Session = Depends(get_db)):
    return crud.get_functions(db)

@app.get("/functions/{function_id}", response_model=schemas.FunctionOut)
def read_one(function_id: int, db: Session = Depends(get_db)):
    func = crud.get_function(db, function_id)
    if not func:
        raise HTTPException(status_code=404, detail="Function not found")
    return func

@app.delete("/functions/{function_id}")
def delete(function_id: int, db: Session = Depends(get_db)):
    success = crud.delete_function(db, function_id)
    if not success:
        raise HTTPException(status_code=404, detail="Function not found")
    return {"deleted": True}
