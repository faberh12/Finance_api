from fastapi import APIRouter, Body, Query, Path, status
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from typing import List
from src.schemas.expense import Expense

expense_router = APIRouter()

expenses = []

@expense_router.post("/expense", tags=["expense"])
def add_expense(expense: Expense):
    expenses.append(expense)
    return {"message": "Expense added successfully"}

@expense_router.get("/expense", tags=["expense"])
def get_expenses():
    return expenses

@expense_router.delete("/expense/{index}", tags=["expense"])
def delete_expense(index: int):
    try:
        expense = expenses.pop(index)
        return {"message": "Expense removed successfully", "expense": expense}
    except IndexError:
        raise HTTPException(status_code=404, detail="Expense not found")