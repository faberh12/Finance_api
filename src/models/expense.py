from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from src.config.database import Base
from sqlalchemy.sql import func


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime, server_default=func.now(), nullable=False)
    description = Column(String(length=64))
    value = Column(Float)
    category = Column(String(length=64))
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="expenses")