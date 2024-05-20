from typing import List,Annotated
from src.models.expense import Expense as ExpenseModel
from src.schemas.expense import Expense
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from src.auth.has_access import security

class ExpenseRepository():
  def __init__(self, db) -> None:
    self.db = db
    
  def get_all_expenses(self,
        credentials: Annotated[HTTPAuthorizationCredentials, 
        Depends(security)],
        offset: int,
        limit: int
        ) -> List[Expense]:
    query = self.db.query(ExpenseModel)
    if(offset is not None):
        query = query.offset(offset)
    if(limit is not None):
        query = query.limit(limit)
    return query.all()

  def get_expense(self, id: int) -> Expense:
          element = self.db.query(ExpenseModel).filter(ExpenseModel.id == id).first()
          return element

  def create_expense(self,
        credentials: Annotated[HTTPAuthorizationCredentials, 
        Depends(security)],
        expense: Expense) -> dict:
      new_expense = ExpenseModel(**expense.model_dump())
      self.db.add(new_expense)
      self.db.commit()
      self.db.refresh(new_expense)
      return new_expense
      
  
    
def remove_expense(self,
        credentials: Annotated[HTTPAuthorizationCredentials, 
        Depends(security)],id: int) -> dict:
    element = self.db.query(ExpenseModel).filter(ExpenseModel.id == id).first()
    self.db.delete(element)
    self.db.commit()
    self.refresh(element)
    return element