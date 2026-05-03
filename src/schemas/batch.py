from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BatchCreate(BaseModel):
    name: str

class BatchOut(BaseModel):
    id: int
    name: str
    institution_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BatchInviteOut(BaseModel):
    token: str
    expires_at: datetime

class JoinBatchRequest(BaseModel):
    token: str
