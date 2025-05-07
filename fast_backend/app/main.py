from fastapi import FastAPI
from .models import user_model
from . import database
from .routes.auth_route import router as auth_router
from .routes.expense_route import router as expense_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


user_model.Base.metadata.create_all(bind=database.engine)


origins = [
    "http://localhost:5173"  # Your production frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # List of allowed origins
    allow_credentials=True,           # Allow cookies and authentication headers
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)

app.include_router(auth_router, prefix='/api/auth', tags=["auth"])
app.include_router(expense_router, prefix='/api/expense', tags=["expense"])