from src.routers.user import user_router
from src.routers.income import income_router
from src.routers.expense import expense_router
from src.middlewares.errror_handler import ErrorHandler
from src.routers.income import incomes
from src.routers.expense import expenses
from fastapi import FastAPI, HTTPException, Body, Path
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Any, Optional


tags_metadata = [
    {
        "name": "web",
        "description": "Endpoints of example",
    },
    {
        "name": "users",
        "description": "Users handling endpoints",  
    },
    {
    "name": "auth",
    "description": "User's authentication",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.title = "FINANCE API"
app.summary = "Product REST API with FastAPI and Python"
app.description = "This is a demonstration of API REST using Python"
app.version = "0.0.1"
app.contact = {
 "name": "Fabian Hernandez Castano",
 "url": "https://github.com/faberh12",
 "email": "fabian.hernandezc@autonoma.edu.co",
} 

app.add_middleware(ErrorHandler)

app.include_router(prefix="/users", router=user_router)
app.include_router(prefix="/incomes", router=income_router)
app.include_router(prefix="/expenses", router=expense_router)

@app.get("/report/basic", tags=["report"])
def basic_report():
    total_income = sum(income.value for income in incomes)
    total_expense = sum(expense.value for expense in expenses)
    balance = total_income - total_expense
    return {"total_income": total_income, "total_expense": total_expense, "balance": balance}

@app.get("/report/extended", tags=["report"])
def extended_report():
    income_by_category = {}
    expense_by_category = {}
    for income in incomes:
        income_by_category.setdefault(income.category, 0)
        income_by_category[income.category] += income.value
    for expense in expenses:
        expense_by_category.setdefault(expense.category, 0)
        expense_by_category[expense.category] += expense.value
    return {"income_by_category": income_by_category, "expense_by_category": expense_by_category}

