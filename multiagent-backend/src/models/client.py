from pydantic import BaseModel , Field , EmailStr
from typing import Optional , List 
from datetime import datetime 


class Client(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name : str 
    email : EmailStr
    phone : Optional[str]
    created_at : Optional[datetime]

#Allows you to use field names in your pydantic models 
    class Config:
        allow_population_by_field_name = True
