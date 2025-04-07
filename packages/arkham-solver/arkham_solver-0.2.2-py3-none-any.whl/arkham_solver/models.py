from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class BalanceResponse(BaseModel):
    """Response model for balance check"""
    balance: float
    has_subscription: bool
    is_active: bool
    subscription_active: bool
    subscription_end: Optional[datetime] = None


class TaskResult(BaseModel):
    """Model for successful task result"""
    solved: bool
    suppressed: bool
    token: str
    variant: Optional[str] = None


class TaskStatusResponse(BaseModel):
    """Response model for task status"""
    created_at: float
    status: str
    task_id: str
    result: Optional[TaskResult] = None
