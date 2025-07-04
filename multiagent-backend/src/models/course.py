from pydantic import BaseModel , Field 
from typing import Optional 
from datetime import datetime 

class Course(BaseModel):
    id : Optional[str] = Field(alias = "_id")
    title : str 
    description : str 
    instructor : str 
    status : str # "upcoming " , " ongoing " , " completed "
    price : float 
    start_time : datetime
    end_time : datetime 


    class Config:
        allow_population_by_field_name = True
