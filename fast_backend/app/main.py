from fastapi import FastAPI
from .models import user_model
from . import database
from .routes.auth_route import router as auth_router
from .routes.expense_route import router as expense_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


user_model.Base.metadata.create_all(bind=database.engine)


origins = [
    "http://localhost:5173"  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,           
    allow_methods=["*"],              
    allow_headers=["*"],              
)

app.include_router(auth_router, prefix='/api/auth', tags=["auth"])
app.include_router(expense_router, prefix='/api/expense', tags=["expense"])