from pydantic import BaseModel , Field , EmailStr
from typing import Optional
from datetime import datetime 

class Enquiries(BaseModel):
    id: Optional[str] = Field(default=None, alias='_id')
    name : str 
    email : EmailStr 
    phone : str 
    query : str 
    status : Optional[str] = "open"