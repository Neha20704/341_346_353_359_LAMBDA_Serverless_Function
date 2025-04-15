from sqlalchemy import Column, Integer, String
from .database import Base

class Function(Base):
    __tablename__ = "functions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    language = Column(String(50))
    route = Column(String(100), unique=True)
    timeout = Column(Integer)
