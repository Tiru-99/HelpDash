from pydantic import BaseModel , Field
from typing import Optional 
from datetime import datetime 

class Payment(BaseModel):
    id : Optional[str] = Field(alias = "_id")
    order_id : str  #References to order 
    payment_date : datetime 
    amount_paid : float 
    payment_method : str #upi , card , etc 

    class Config : 
        allow_population_by_field_name = True