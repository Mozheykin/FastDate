from pydantic import BaseModel
from enum import Enum

class Gender(Enum):
    male = 'male'
    female = 'female'

class Customer(BaseModel):
    user_id: int                 
    username: str
    balance: float                 
    age: int                 
    gender:str                 
    language: str
    info: str                 
    photo: str                 
    location: str
    range: int                 
    is_gold: bool
    is_active: bool

class CustomerView(BaseModel):
    id: int
    user_id: int                 
    username: str
    balance: float                 
    age: int                 
    gender:str                 
    language: str
    info: str                 
    photo: str                 
    location: str
    range: int                 
    is_gold: bool
    is_active: bool