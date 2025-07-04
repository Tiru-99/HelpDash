from pydantic import BaseModel , Field 
from typing import Optional 
from datetime import datetime 

class ClassSession(BaseModel):
    id : Optional[str] = Field(alias = "_id")
    client_id : str #Reference to Client
    course_id : str #Reference To Course
    date : datetime 
    instructor : str 
    status : str # "scheduled " , "completed" , "cancelled"

    class Config:
        allow_population_by_field_name = True
