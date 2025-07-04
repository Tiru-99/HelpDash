from typing import Type 
from crewai.tools import BaseTool 
from bson import ObjectId
from pydantic import BaseModel , Field
from db.mongo import db

orders_collection = db["orders"]

class GetOrderByIdInput(BaseModel) :
    order_id : str = Field(... , description = "Order id required to get the order ")


class GetOrderByIdTool(BaseTool):
    name: str = "Get Order by ID"
    description: str = "Fetch order details using order ID"
    args_schema: Type[BaseModel] = GetOrderByIdInput

    def _run(self, order_id: str) -> str:
        try:
        
            order = orders_collection.find_one({"_id": ObjectId(order_id)})

            if order:
                order["_id"] = str(order["_id"])  # make ObjectId JSON-safe
                return order
            else:
                return f"No order found with ID: {order_id}"

        except Exception as e:
            return f"Error retrieving order {order_id}: {str(e)}"
        
        
        

class GetOrderByClientIdInput(BaseModel) :
    client_id : str = Field(... , description = "Client id required to get the order")

class GetOrderByClient(BaseTool):
    name: str = "Get order by client ID"
    description: str = "Fetch all orders placed by a specific client ID"
    args_schema: Type = GetOrderByClientIdInput

    def _run(self, client_id: str) -> str:
        try:
            orders = list(orders_collection.find({"client_id": client_id}))

            if not orders:
                return f"No orders found for client ID: {client_id}"

            for order in orders:
                order["_id"] = str(order["_id"])  # make ObjectId JSON-serializable

            return orders

        except Exception as e:
            return f"Error retrieving orders for client ID {client_id}: {str(e)}"      
