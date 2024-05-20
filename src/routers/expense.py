from fastapi import APIRouter, Body, Query, Path, status
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.expense import Expense
from src.config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from src.repositories.expense import ExpenseRepository

expense_router = APIRouter()

@expense_router.get("/",tags=['expenses'],response_model=List[Expense],description="Returns all expenses")
def get_all_expenses(
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)
        ) -> List[Expense]:
    db = SessionLocal()
    result = ExpenseRepository(db).get_all_expenses(offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
def create_expense(expense: Expense = Body()) -> dict:
    db = SessionLocal()
    new_expense = ExpenseRepository(db).create_expense(expense)
    return JSONResponse(content={
        "message": "The expense was successfully created",
        "data": jsonable_encoder(new_expense)
    }, status_code=status.HTTP_201_CREATED)
    
@expense_router.delete('/{id}',tags=['expenses'],response_model=dict,description="Removes specific expense")
def remove_expense(id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = ExpenseRepository(db).get_expense(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested expense was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    ExpenseRepository(db).remove_expense(id)
    return JSONResponse(content={
        "message": "The expense wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)