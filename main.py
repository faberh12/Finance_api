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

class User(BaseModel):
    id: Optional[int] = Field(default=None, title="User ID (auto-generated)")
    email: str = Field(default=None, title="User email address")
    first_name: str = Field(default=None, title="User first name")
    last_name: str = Field(default=None, title="User last name")
    password: str = Field(default=None, min_length=8, title="User password")
    active: bool = Field(default=True, title="User active status")

class Income(BaseModel):
    date: str
    description: str
    value: float
    category: str

class Expense(BaseModel):
    date: str
    description: str
    value: float
    category: str

@validator("email")
def validate_email(cls, value):
        if not value.endswith("@example.com"):
            raise ValueError("Only example.com email addresses are allowed")
        return value

user = {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword",
    "active": True
}

@app.get('/users', tags=['users'], response_model=User, description="Returns the user")
def get_user() -> User:
    return User(**user)

@app.put('/users', tags=['users'], response_model=User, description="Updates the user data")
def update_user(user: User = Body(...)) -> User:
    for field, value in user.dict().items():
        if value is not None:
            setattr(user, field, value)
    return user

@app.post('/users', tags=['users'], response_model=User, description="This endpoint is not available for single-user mode")
def create_user(user: User = Body(...)) -> User:
    raise HTTPException(status_code=405, detail="Creating users is not allowed in single-user mode")

@app.delete('/users/{id}', tags=['users'], response_model=User, description="This endpoint is not available for single-user mode")
def delete_user(id: int = Path(..., ge=1)) -> User:
    raise HTTPException(status_code=405, detail="Deleting users is not allowed in single-user mode")


incomes = []
expenses = []

@app.post("/income", tags=["income"])
def add_income(income: Income):
    incomes.append(income)
    return {"message": "Income added successfully"}

@app.post("/expense", tags=["expense"])
def add_expense(expense: Expense):
    expenses.append(expense)
    return {"message": "Expense added successfully"}

@app.get("/income", tags=["income"])
def get_incomes():
    return incomes

@app.get("/expense", tags=["expense"])
def get_expenses():
    return expenses

@app.delete("/income/{index}", tags=["income"])
def delete_income(index: int):
    try:
        income = incomes.pop(index)
        return {"message": "Income removed successfully", "income": income}
    except IndexError:
        raise HTTPException(status_code=404, detail="Income not found")

@app.delete("/expense/{index}", tags=["expense"])
def delete_expense(index: int):
    try:
        expense = expenses.pop(index)
        return {"message": "Expense removed successfully", "expense": expense}
    except IndexError:
        raise HTTPException(status_code=404, detail="Expense not found")

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

