from pydantic import BaseModel

class FunctionCreate(BaseModel):
    name: str
    language: str
    route: str
    timeout: int

class FunctionOut(FunctionCreate):
    id: int

    class Config:
        orm_mode = True
