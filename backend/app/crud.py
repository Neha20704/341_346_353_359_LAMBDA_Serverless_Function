from sqlalchemy.orm import Session
from . import models, schemas
from .models import ExecutionMetric


def get_functions(db: Session):
    return db.query(models.Function).all()

def get_function(db: Session, function_id: int):
    return db.query(models.Function).filter(models.Function.id == function_id).first()

def create_function(db: Session, function: schemas.FunctionCreate):
    db_func = models.Function(**function.dict())
    db.add(db_func)
    db.commit()
    db.refresh(db_func)
    return db_func

def delete_function(db: Session, function_id: int):
    func = db.query(models.Function).filter(models.Function.id == function_id).first()
    if func:
        db.delete(func)
        db.commit()
        return True
    return False


def log_metric(db: Session, function_id: int, time_taken: float, was_error: bool, error_message: str = None):
    metric = ExecutionMetric(
        function_id=function_id,
        execution_time=time_taken,
        was_error=was_error,
        error_message=error_message
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

