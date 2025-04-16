from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from .schemas import ExecuteFunctionRequest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../executor")))
import runner  # ✅ this imports runner.py from the executor/ folder

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
    try:
        return crud.create_function(db, function)
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Internal Server Error")


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

@app.post("/functions/execute")
def execute_function(request: ExecuteFunctionRequest, db: Session = Depends(get_db)):
    function_id = request.id
    args = request.args or []
    use_gvisor = request.use_gvisor

    func = db.query(models.Function).filter(models.Function.id == function_id).first()
    if not func:
        raise HTTPException(status_code=404, detail="Function not found")

    output, error = runner.run_function(
        func.language, func.route,
        args=args,
        timeout=func.timeout,
        use_gvisor=use_gvisor
    )
    return {"output": output, "error": error}
