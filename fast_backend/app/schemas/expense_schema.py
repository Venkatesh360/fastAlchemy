from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ExpenseBase(BaseModel):
    category: str
    amount: float
    description: Optional[str] = None


class CreateExpense(ExpenseBase):
    pass


class UpdateExpense(BaseModel):
    expense_id: int
    category: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None


class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  


class ExpenseListResponse(BaseModel):
    expenses: List[ExpenseResponse]
