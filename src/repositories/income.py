from typing import List
from src.models.income import Income as IncomeModel
from src.schemas.income import Income
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Depends
from src.auth.has_access import security

class IncomeRepository():
  def __init__(self, db) -> None:
    self.db = db
    
  def get_all_incomes(self,
        credentials: Annotated[HTTPAuthorizationCredentials, 
        Depends(security)],
        offset: int ,
        limit: int
        ) -> List[Income]:
    query = self.db.query(IncomeModel)
    if(offset is not None):
        query = query.offset(offset)  
    if(limit is not None):
        query = query.limit(limit)
    return query.all()
  
  def get_income(self, id: int) -> Income:
          element = self.db.query(IncomeModel).filter(IncomeModel.id == id).first()
          return element
    
  def create_income(self,
                    credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
                    income: Income) -> dict:
      new_income = IncomeModel(**income.model_dump())
      self.db.add(new_income)
      self.db.commit()
      self.db.refresh(new_income)
      return new_income
      
  def remove_income(self, 
                    credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
                    id: int) -> dict:
      element = self.db.query(IncomeModel).filter(IncomeModel.id == id).first()
      self.db.delete(element)
      self.db.commit()
      return element