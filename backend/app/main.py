from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
#from fastapi.responses import JSONResponse
from . import models, schemas, crud, database
from .schemas import ExecuteFunctionRequest
import time
from .crud import log_metric


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

    start = time.time()
    output, error = runner.run_function(
        func.language, func.route,
        args=args,
        timeout=func.timeout,
        use_gvisor=use_gvisor
    )
    duration = time.time() - start
    was_error = bool(error)
    
    log_metric(db, function_id=func.id, time_taken=duration, was_error=was_error, error_message=error if was_error else None)

    return {"output": output, "error": error}

#endpoint to view metrics
@app.get("/metrics", response_model=list[schemas.MetricOut])
def get_all_metrics(db: Session = Depends(get_db)):
    return db.query(models.ExecutionMetric).all()

#Metrics aggregation
@app.get("/metrics/summary")
def get_metric_summary(db: Session = Depends(get_db)):
    summary = db.query(
        models.ExecutionMetric.function_id,
        func.count().label("total_calls"),
        func.avg(models.ExecutionMetric.execution_time).label("avg_time"),
        func.sum(func.if_(models.ExecutionMetric.was_error == True, 1, 0)).label("error_count")
    ).group_by(models.ExecutionMetric.function_id).all()

    results = [
        {
            "function_id": s.function_id,
            "total_calls": s.total_calls,
            "avg_time": round(s.avg_time, 3),
            "error_count": int(s.error_count)
        } for s in summary
    ]
    return JSONResponse(content=results)
#update function
@app.put("/functions/{function_id}", response_model=schemas.FunctionOut)
def update_function(function_id: int, function: schemas.FunctionCreate, db: Session = Depends(get_db)):
    func = crud.get_function(db, function_id)
    if not func:
        raise HTTPException(status_code=404, detail="Function not found")

    # Update fields
    func.name = function.name
    func.language = function.language
    func.route = function.route
    func.timeout = function.timeout

    db.commit()
    db.refresh(func)
    return func
