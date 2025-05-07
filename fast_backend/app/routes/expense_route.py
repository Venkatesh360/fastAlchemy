from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import database
from ..utils import utils
from ..schemas import expense_schema
from ..models.user_model import Expense

router = APIRouter()


# Dependency to get DB session
def get_db():
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
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    return {"expenses": expenses}


@router.post("/create_expense", response_model=expense_schema.ExpenseResponse)
def create_expense(
    exp_obj: expense_schema.CreateExpense,
    user_id: int = Depends(utils.decode_token),
    db: Session = Depends(get_db)
):
    print("received")
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
    print(exp_obj)
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
