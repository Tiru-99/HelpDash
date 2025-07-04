from typing import Type
from crewai.tools import BaseTool 
from pydantic import BaseModel , Field , EmailStr , root_validator
from db.mongo import db

collection = db["clients"]
service_collection = db["classes"]

class SearchClientInput(BaseModel):
    email : EmailStr = Field(None , description = "Email Input type for search client function")
    name : str = Field(None , description = "Name input type for search client function ")
    phone : str = Field(None , description = "Phone input type for search client function")

    @root_validator(pre = True)
    def at_least_one_field_required(cls, values):
        if not any([values.get("email"), values.get("name"), values.get("phone")]):
            raise ValueError("At least one of email, name, or phone must be provided")
        return values
    
class GetClientEnrolledServicesInput(BaseModel):
    client_id : str = Field(... , description = "Client input id for getting enrolled services")
    
    

class SearchClient(BaseTool):
    name : str = "Search Client By Email , Phone or Name "
    description : str = "Get order data by order id "
    args_schema : Type = SearchClientInput

    def _run(self , email : str = None , phone : str = None , name : str = None) -> str :
        try:
            # Check and query by the first available parameter
            if email:
                client_data = collection.find_one({"email": email})
            elif phone:
                client_data = collection.find_one({"phone": phone})
            elif name:
                client_data = collection.find_one({"name": name})
            else:
                return "Please provide at least one of email, phone, or name"

            if client_data:
                client_data["_id"] = str(client_data["_id"])
                return client_data
            else:
                return "Client not found."

        except Exception as e:
            return f"Error while searching: {str(e)}"
         
         


class GetClientEnrolledService(BaseTool):
    name: str = "Get Client's Enrolled Services"
    description: str = "Fetch all enrolled services (orders) for a given client ID"
    args_schema: Type = GetClientEnrolledServicesInput

    def _run(self, client_id: str) -> str:
        try:
            orders = list(service_collection.find({"client_id": client_id}))

            if not orders:
                return f"No enrolled services found for client {client_id}"

            # convert ObjectId to string for safety
            for order in orders:
                order["_id"] = str(order["_id"])

            return orders

        except Exception as e:
            return f"Error fetching services for client {client_id}: {str(e)}"