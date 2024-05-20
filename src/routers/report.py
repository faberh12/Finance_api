from fastapi import APIRouter, HTTPException,Path, status, Depends
from sqlalchemy.orm import Session
from src.config.database import SessionLocal
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.repositories.report import ReportRepository
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security

report_router = APIRouter()

@report_router.get("/basic", tags=['reports'],response_model=dict, description="Returns basic report")
def get_basic_report(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)]):
    db: Session = SessionLocal()
    try:
        report_data = ReportRepository(db).get_basic_report(credentials)

        return JSONResponse(content=jsonable_encoder(report_data), status_code=200)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@report_router.get("/extended", tags=['reports'],response_model=dict, description="Returns extended report")
def get_extended_report(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)]):
    db: Session = SessionLocal()
    try:
        report_data = ReportRepository(db).get_extended_report(credentials)
        return JSONResponse(content=jsonable_encoder(report_data), status_code=200)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@report_router.delete('/{id}',tags=['reports'],response_model=dict,description="Removes specific report")
def remove_report(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
                    id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = ReportRepository(db).get_by_id(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested report was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    ReportRepository(db).remove_report(id)
    return JSONResponse(content={
        "message": "The report wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)