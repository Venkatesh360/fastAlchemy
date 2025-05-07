from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base  


class TimestampMixin:
    """
            Mixin that adds automatic timestamp fields for creation and last update.

            Attributes:
                created_at (DateTime): The timestamp when the record was created.
                    - Automatically set to the current time when the row is inserted.
                
                updated_at (DateTime): The timestamp when the record was last updated.
                    - Automatically set to the current time when the row is inserted.
                    - Automatically updated to the current time whenever the row is updated.
    """
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class User(Base, TimestampMixin):
    """
    Database model for a user.

    Inherits:
        Base (declarative_base): SQLAlchemy declarative base.
        TimestampMixin: Adds `created_at` and `updated_at` timestamp fields.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        username (str): Unique username of the user.
        email (str): Unique email address of the user.
        hashed_password (str): Hashed version of the user's password.
        expenses (List[Expense]): List of expenses associated with the user.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    expenses = relationship('Expense', back_populates='owner', cascade="all, delete-orphan")


class Expense(Base, TimestampMixin):
    """
    Database model for an expense entry.

    Inherits:
        Base (declarative_base): SQLAlchemy declarative base.
        TimestampMixin: Adds `created_at` and `updated_at` timestamp fields.

    Attributes:
        id (int): Primary key, unique identifier for the expense.
        category (str): Category of the expense (e.g., Food, Travel, Utilities).
        amount (float): Monetary amount of the expense.
        description (str, optional): Optional text description for the expense.
        user_id (int): Foreign key referencing the ID of the user who owns this expense.
        owner (User): Relationship to the `User` model representing the owner of the expense.
    """
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    owner = relationship('User', back_populates='expenses')
