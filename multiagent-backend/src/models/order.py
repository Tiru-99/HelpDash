from pydantic import BaseModel , Field , Optional  
from typing import List
from datetime import datetime 

class Order(BaseModel):
    id : Optional[str] = Field(alias = "_id")
    client_id : str #Reference to Client 
    course_id : str #Reference to Course
    amount : float 
    status : str #paid #pending 
    created_at : Optional[datetime]

    class Config:
        allow_population_by_field_name = True
