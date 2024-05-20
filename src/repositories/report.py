from typing import List,Annotated
from src.models.income import Income
from src.models.expense import Expense
from src.models.report import Report as ReportModel
from src.schemas.report import Report
from sqlalchemy import func, text
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from src.auth.has_access import security



class ReportRepository():
  def __init__(self, db) -> dict:
    self.db = db
    
  def get_basic_report(self,
        credentials: Annotated[HTTPAuthorizationCredentials, 
        Depends(security)]):
    total_incomes = self.db.query(Income).count() or 0
    total_income_value = self.db.query(func.sum(Income.value)).scalar() or 0
    total_expenses = self.db.query(Expense).count() or 0
    total_expense_value = self.db.query(func.sum(Expense.value)).scalar() or 0
    total_balance = total_income_value - total_expense_value

    report_data = {
        "total_incomes": total_incomes,
        "total_income_value": total_income_value,
        "total_expenses": total_expenses,
        "total_expense": total_expense_value,
        "total_balance": total_balance
    }

    new_report = ReportModel(
        type="basic",
        description=report_data
    )
    self.db.add(new_report)
    self.db.commit()
    self.db.refresh(new_report)

    return new_report
  
  def get_extended_report(self,
        credentials: Annotated[HTTPAuthorizationCredentials, 
        Depends(security)])->dict:
    income_by_category = self.db.query(
        Income.category,
        func.json_arrayagg(
            text("JSON_OBJECT('id', id, 'date', date, 'description', description, 'value', value)")
        ).label('json_data')
    ).group_by(Income.category).all()
    
    expense_by_category = self.db.query(
        Expense.category,
        func.json_arrayagg(
            text("JSON_OBJECT('id', id, 'date', date, 'description', description, 'value', value)")
        ).label('json_data')
    ).group_by(Expense.category).all()

    income_report = {category: data for category, data in income_by_category}
    expense_report = {category: data for category, data in expense_by_category}

    report_data = {
        "incomes": income_report,
        "expenses": expense_report
    }

    new_report = ReportModel(
        type="extended",
        description=report_data 
    )
    self.db.add(new_report)
    self.db.commit()
    self.db.refresh(new_report)

    return new_report
  
  def get_report(self, id: int) -> Report:
        element = self.db.query(ReportModel).filter(ReportModel.id == id).first()
        return element
  
  def remove_report(self,id: int) -> dict:
    element = self.db.query(ReportModel).filter(ReportModel.id == id).first()
    self.db.delete(element)
    self.db.commit()
    return element