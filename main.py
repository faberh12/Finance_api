from src.routers.user import user_router
from src.routers.income import income_router
from src.routers.expense import expense_router
from src.routers.report import report_router
from src.middlewares.errror_handler import ErrorHandler
from fastapi import FastAPI
from src.config.database import Base, engine

tags_metadata = [
    {
        "name": "users",
        "description": "Users handling endpoints",  
    },
    {
        "name": "auth",
        "description": "User's authentication",
    },
    {
        "name": "incomes",
        "description": "User's incomes",
    },
    {
        "name": "expenses",
        "description": "User's expenses",
    },
    {
        "name": "reports",
        "description": "User's reports of incomes and expenses",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.title = "FINANCE API"
app.summary = "Product REST API with FastAPI and Python"
app.description = "This is a demonstration of API REST using Python"
app.version = "0.0.1"
app.contact = {
 "names": "Fabian Hernandez Castano, yeferson valencia aristizabal",
 "url": "https://github.com/faberh12",
 "emails": "fabian.hernandezc@autonoma.edu.co, yeferson.valenciaa@autonoma.edu.co",
} 

Base.metadata.create_all(bind=engine)

app.add_middleware(ErrorHandler)

app.include_router(prefix="/users", router=user_router)
app.include_router(prefix="/incomes", router=income_router)
app.include_router(prefix="/expenses", router=expense_router)
app.include_router(prefix="/reports", router=report_router)

