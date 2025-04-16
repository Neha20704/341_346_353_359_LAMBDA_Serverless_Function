from pydantic import BaseModel
from typing import List, Optional

class FunctionCreate(BaseModel):
    name: str
    language: str
    route: str
    timeout: int

class FunctionOut(FunctionCreate):
    id: int

    class Config:
        orm_mode = True

# Create a model for the /functions/execute request body
class ExecuteFunctionRequest(BaseModel):
    id: int  # Expecting an 'id' field
    args: Optional[List[str]] = None
    use_gvisor: Optional[bool] = False