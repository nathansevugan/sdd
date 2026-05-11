from pydantic import BaseModel
from typing import Optional

class WisdomResponse(BaseModel):
    id: int
    title: str
    description: str
    
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: str
    request_id: Optional[str] = None
    retry_after: Optional[int] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    database: str
    total_wisdom: Optional[int] = None
