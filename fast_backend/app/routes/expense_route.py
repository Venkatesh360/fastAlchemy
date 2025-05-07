from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import database
from ..utils import utils
from ..schemas import expense_schema
from ..models.user_model import Expense

router = APIRouter()


def get_db():
    """
    Dependency that provides a SQLAlchemy database session.

    Yields:
        Session: An active SQLAlchemy session that can be used to interact with the database.

    Ensures the session is properly closed after the request is completed.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/get_expense", response_model=expense_schema.ExpenseListResponse)
def get_user_expenses(
    user_id: int = Depends(utils.decode_token),
    db: Session = Depends(get_db)
):
    """"
    Fetch all expenses for the authenticated user.
    
    Args:
        user_id(int): ID of the authenticated user, extracted from the JWT token via the `decode_token` dependency.
        db(Session): SQLAlchemy database session, provided by the `get_db` dependency

    Returns:
        dict:
            A dictionary containing a list of expense objects under the key `"expenses"`, matching the response model `ExpenseListResponse`.
    
    """
    
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    return {"expenses": expenses}


@router.post("/create_expense", response_model=expense_schema.ExpenseResponse, )
def create_expense(
    exp_obj: expense_schema.CreateExpense,
    user_id: int = Depends(utils.decode_token),
    db: Session = Depends(get_db)
):
    """
    Create a new expense entry for the authenticated user.
    
    Args:
        exp_obj (CreateExpense): Pydantic model containing the expense details (category, amount, description).
        user_id (int): ID of the authenticated user, extracted from the JWT token via the `decode_token` dependency.
        db (Session): SQLAlchemy database session, provided by the `get_db` dependency.

    Returns:
        Expense: The newly created expense object, returned in the format defined by `ExpenseResponse`.
    """
    new_expense = Expense(
        category=exp_obj.category,
        amount=exp_obj.amount,
        description=exp_obj.description,
        user_id=user_id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.put("/update_expense", response_model=expense_schema.ExpenseResponse)
def update_expense(
    exp_obj: expense_schema.UpdateExpense,
    user_id: int = Depends(utils.decode_token),
    db: Session = Depends(get_db)
):
    """
    Update an existing expense for the authenticated user.

    Args:
        exp_obj (UpdateExpense): Pydantic model containing the expense ID and optional fields to update (amount, category, description).
        user_id (int): ID of the authenticated user, extracted from the JWT token via the `decode_token` dependency.
        db (Session): SQLAlchemy database session, provided by the `get_db` dependency.

    Returns:
        Expense: The updated expense object in the format defined by `ExpenseResponse`.

    Raises:
        HTTPException: If the expense does not exist or does not belong to the user.
    """
    expense = db.query(Expense).filter(
        (Expense.id == exp_obj.expense_id) & (Expense.user_id == user_id)
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense doesn't exist")

    if exp_obj.amount is not None:
        expense.amount = exp_obj.amount #type: ignore

    if exp_obj.category is not None:
        expense.category = exp_obj.category #type: ignore

    if exp_obj.description is not None:
        expense.description = exp_obj.description #type: ignore

    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/delete_expense/{expense_id}")
def delete_expense(
    expense_id: int,
    user_id: int = Depends(utils.decode_token),
    db: Session = Depends(get_db)
):
    """
    Delete an existing expense for the authenticated user.

    Args:
        expense_id (int): ID of the expense to be deleted, provided as a path parameter.
        user_id (int): ID of the authenticated user, extracted from the JWT token via the `decode_token` dependency.
        db (Session): SQLAlchemy database session, provided by the `get_db` dependency.

    Returns:
        dict: A success message confirming deletion along with the category and description of the deleted expense.

    Raises:
        HTTPException: If the expense does not exist or does not belong to the user.
    """
    expense = db.query(Expense).filter(
        (Expense.id == expense_id) & (Expense.user_id == user_id)
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense doesn't exist")

    db.delete(expense)
    db.commit()

    return {
        "message": (
            f"Expense deleted successfully - Category: '{expense.category}', "
            f"Description: '{expense.description}'"
        )
    }
