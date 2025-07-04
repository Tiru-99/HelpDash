from pydantic import BaseModel, Field
from typing import Type, Optional
from datetime import datetime, timezone
from crewai.tools import BaseTool
import uuid

from db.mongo import db

clients_collection  = db["clients"]
courses_collection  = db["courses"]
orders_collection   = db["orders"]

class SmartCreateOrderInput(BaseModel):
    client_name: str = Field(..., description="Exact name of the client")
    course_name: str = Field(..., description="Exact title of the course")
    amount: Optional[float] = Field(None, description="Order amount; defaults to course price")
    status: str = Field(default="pending", description="Order payment status")


class SmartCreateOrderTool(BaseTool):
    name: str = "smart_create_order"
    description: str = "Create an order by resolving client & course names to IDs"
    args_schema: Type = SmartCreateOrderInput

    def _run(
        self,
        client_name: str,
        course_name: str,
        amount: Optional[float] = None,
        status: str = "pending"
    ) -> str:
        try:
            # Resolve client
            client = clients_collection.find_one({"name": client_name})
            if not client:
                return f"Client with name '{client_name}' not found."

            # Resolve course
            course = courses_collection.find_one({"title": course_name})
            if not course:
                return f"Course with name '{course_name}' not found."

            # Default amount to course price if not supplied
            order_amount = amount if amount is not None else course.get("price", 0)

            order_doc = {
                "_id": f"ord{uuid.uuid4().hex[:6]}",
                "client_id": client["_id"],        # reference to clients collection
                "course_id": course["_id"],        # reference to courses collection
                "amount": order_amount,
                "status": status,
                "created_at": datetime.now(timezone.utc).isoformat()
            }

            # Insert
            orders_collection.insert_one(order_doc)

            return (
                f"Order `{order_doc['_id']}` created for client "
                f"`{client_name}` on course `{course_name}` (₹{order_amount})."
            )

        except Exception as e:
            return f"Failed to create order: {str(e)}"
