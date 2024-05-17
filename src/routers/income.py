from fastapi import APIRouter, Body, Query, Path, status
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.income import Income

income_router = APIRouter()

incomes = []

@income_router.post("/income", tags=["income"])
def add_income(income: Income):
    incomes.append(income)
    return {"message": "Income added successfully"}
  
@income_router.get("/income", tags=["income"])
def get_incomes():
    return incomes
  
@income_router.delete("/income/{index}", tags=["income"])
def delete_income(index: int):
    try:
        income = incomes.pop(index)
        return {"message": "Income removed successfully", "income": income}
    except IndexError:
        raise HTTPException(status_code=404, detail="Income not found")