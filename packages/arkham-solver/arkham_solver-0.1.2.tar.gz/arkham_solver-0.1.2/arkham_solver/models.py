from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BalanceResponse(BaseModel):
    """Response model for balance check"""
    balance: float
    has_subscription: bool
    is_active: bool
    subscription_active: bool
    subscription_end: Optional[datetime] = None

class SolveResponse(BaseModel):
    """Response model for solve request"""
    solved: bool
    suppressed: bool
    token: str
    variant: Optional[str] = None