from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.config.database import Base

class Income(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime, server_default=func.now(), nullable=False)
    description = Column(String(length=64))
    value = Column(Float)
    category = Column(String(length=64))
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="incomes")