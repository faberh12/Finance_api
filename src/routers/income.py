from fastapi import APIRouter, Body, Query, Path, status
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.income import Income
from src.config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from src.repositories.income import IncomeRepository

income_router = APIRouter()

@income_router.get("/",tags=['incomes'],response_model=List[Income],description="Returns all incomes")
def get_all_incomes(
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)
        ) -> List[Income]:
    db = SessionLocal()
    result = IncomeRepository(db).get_all_incomes(offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@income_router.post('/',tags=['incomes'],response_model=dict,description="Creates a new income")
def create_income(income: Income = Body()) -> dict:
    db = SessionLocal()

    new_income = IncomeRepository(db).create_income(income)
    return JSONResponse(content={
        "message": "The income was successfully created",
        "data": jsonable_encoder(new_income)
    }, status_code=status.HTTP_201_CREATED)
    
@income_router.delete('/{id}',tags=['incomes'],response_model=dict,description="Removes specific income")
def remove_income(id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = IncomeRepository(db).get_income(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested income was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    IncomeRepository(db).remove_income(id)
    return JSONResponse(content={
        "message": "The income wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)