from pydantic import BaseModel
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str


class FoodCreate(BaseModel):
    food_name: str
    quantity: str
    location: str


# Response models
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class FoodResponse(BaseModel):
    id: int
    food_name: str
    quantity: str
    location: str
    expiry_estimate: int

    class Config:
        from_attributes = True