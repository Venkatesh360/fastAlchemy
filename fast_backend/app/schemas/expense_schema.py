from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ExpenseBase(BaseModel):
    """
    Base model for Expense-related data, used as a foundation for creating and updating expenses.

    Attributes:
        category (str): The category of the expense (e.g., 'Food', 'Travel').
        amount (float): The monetary amount of the expense.
        description (Optional[str]): Optional description of the expense.
    """
    category: str
    amount: float
    description: Optional[str] = None


class CreateExpense(ExpenseBase):
    """
    Pydantic model for creating an expense.

    Inherits:
        ExpenseBase: Contains category, amount, and description fields.

    No additional fields, just used for enforcing validation on input data when creating an expense.
    """
    pass


class UpdateExpense(BaseModel):
    """
    Pydantic model for updating an existing expense.

    Attributes:
        expense_id (int): ID of the expense to update.
        category (Optional[str]): New category for the expense (if updating).
        amount (Optional[float]): New amount for the expense (if updating).
        description (Optional[str]): New description for the expense (if updating).
    """
    expense_id: int
    category: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None


class ExpenseResponse(ExpenseBase):
    """
    Pydantic model for the response when retrieving an expense.

    Inherits:
        ExpenseBase: Contains category, amount, and description fields.

    Attributes:
        id (int): The ID of the expense.
        created_at (datetime): Timestamp of when the expense was created.
        updated_at (datetime): Timestamp of when the expense was last updated.

    Config:
        orm_mode (bool): Enables compatibility with SQLAlchemy models (by converting ORM objects to Pydantic models).
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  


class ExpenseListResponse(BaseModel):
    """
    Pydantic model for returning a list of expenses in the response.

    Attributes:
        expenses (List[ExpenseResponse]): A list of expense objects, each of which follows the `ExpenseResponse` model.
    """
    expenses: List[ExpenseResponse]
