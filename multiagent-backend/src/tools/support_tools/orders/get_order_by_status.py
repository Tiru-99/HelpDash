from typing import Type, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from db.mongo import db

orders_collection = db["orders"]

class GetOrderByStatusInput(BaseModel):
    status: str = Field(..., description="Status required to filter (e.g., paid, pending)")
    order_id: Optional[str] = Field(
        None,
        description="If provided, filter by this specific order_id AND status"
    )

class GetOrderByStatus(BaseTool):
    name: str = "get_orders_by_status"
    description: str = (
        "Fetch orders by status alone, or by status + order_id if the caller provides it."
    )
    args_schema: Type = GetOrderByStatusInput

    def _run(self, **kwargs) -> str:
        status  = kwargs.get("status")
        order_id = kwargs.get("order_id")

        # Build query dynamically
        query = {"status": status}
        if order_id:               
            query["_id"] = ObjectId(order_id)

        try:
            orders = list(orders_collection.find(query))

            if not orders:
                return f"No orders found for query: {query}"

            for o in orders:
                o["_id"] = str(o["_id"])  # JSON‑safe

            return orders

        except Exception as e:
            return f"Error retrieving orders: {str(e)}"
