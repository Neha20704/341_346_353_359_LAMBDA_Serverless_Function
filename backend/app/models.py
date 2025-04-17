from sqlalchemy import Column, Integer, Float, Boolean, String, DateTime, ForeignKey
from datetime import datetime
from .database import Base

class Function(Base):
    __tablename__ = "functions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    language = Column(String(50))
    route = Column(String(100), unique=True)
    timeout = Column(Integer)


class ExecutionMetric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    function_id = Column(Integer, ForeignKey("functions.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    execution_time = Column(Float)
    was_error = Column(Boolean)
    error_message = Column(String(255), nullable=True)
