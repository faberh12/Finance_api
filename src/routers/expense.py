from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from src.schemas.expense import Expense
from src.config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from src.repositories.expense import ExpenseRepository
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security

expense_router = APIRouter()

@expense_router.get("/",tags=['expenses'],response_model=List[Expense],description="Returns all expenses")
def get_all_expenses(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)
        ) -> List[Expense]:
    db = SessionLocal()
    result = ExpenseRepository(db).get_all_expenses(credentials,offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@expense_router.post('/',tags=['expenses'],response_model=dict,description="Creates a new expense")
def create_expense(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],expense: Expense = Body()) -> dict:
    db = SessionLocal()
    new_expense = ExpenseRepository(db).create_expense(credentials,expense)
    return JSONResponse(content={
        "message": "The expense was successfully created",
        "data": jsonable_encoder(new_expense)
    }, status_code=status.HTTP_201_CREATED)
    
@expense_router.delete('/{id}',tags=['expenses'],response_model=dict,description="Removes specific expense")
def remove_expense(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
                    id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = ExpenseRepository(db).get_expense(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested expense was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    ExpenseRepository(db).remove_expense(credentials,id)
    return JSONResponse(content={
        "message": "The expense wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)