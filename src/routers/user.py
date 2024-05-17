from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from fastapi import APIRouter, Body, Query, Path, status
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.user import User

user_router = APIRouter()

users = [
    {
        "id": 1234  , 
        "email": "pepe@example.com",
        "name": "Pepe Pimentón",
        "password": "xxx",
        "is_active": True
    }    
]

@user_router.get('/', tags=['users'], response_model=List[User], description="Returns all users")
def get_all_users() -> List[User]:
    return users

@user_router.put('/{id}', tags=['users'], response_model=dict, description="Updates the user data")
def update_user(id: int = Path(ge=1),user: User = Body()) -> dict:
    for element in users:
        if element['id'] == id:
            element['name'] = user.name
            element['email'] = user.email
            element['pasword'] = user.pasword
            element['is_active'] = user.is_active
            return JSONResponse(content={
                "message": "The product was updated successfully",
                "data": element
            }, status_code=200)
    return JSONResponse(content={
        "message": "The product does not exist",
        "data": None
    }, status_code=404)

@user_router.post('/', tags=['users'], response_model=dict, description="creates a new user")
def create_user(user: User = Body()) -> dict:
    users.append(user.model_dump())
    return JSONResponse(content={
        "message": "The product was created successfully",
        "data": user.model_dump()
    }, status_code=201)

@user_router.delete('/{id}',tags=['users'],response_model=dict,description="Removes specific user")
def remove_product(id: int = Path(ge=1)) -> dict:
    for element in users:
        if element['id'] == id:
            users.remove(element)
        return JSONResponse(content={"message": "The product wass removed successfully","data": None}, status_code=204)
    return JSONResponse(content={"message": "The product does not exists","data": None}, status_code=404)


class UserCreate (BaseModel):
    name: str = Field(min_length=4, max_length=60, title="Name of the user")
    email: EmailStr = Field(min_length=6, max_length=64, title="Email of the user")
    password: str = Field(max_length=64, title="Password of the user")

class UserLogin (BaseModel):
    email: EmailStr = Field(min_length=6, max_length=64, alias="username",
    title="Email of the user")
    password: str = Field(min_length=4, title="Password of the user")
