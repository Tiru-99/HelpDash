from crewai.tools import BaseTool 
from db.mongo import db
from typing import Type 
from pydantic import BaseModel

payments_collection = db["payments"]
orders_collection = db["orders"]


class NoArgsSchema(BaseModel):
    pass

class TotalRevenueTool(BaseTool):
    name: str = "total_revenue"
    description: str = "Get total revenue from all successful payments"
    args_schema: Type = NoArgsSchema  # No input needed

    def _run(self) -> str:
        try:
            revenue = payments_collection.aggregate([
                {"$group": {"_id": None, "total": {"$sum": "$amount_paid"}}}
            ])
            total = next(revenue, {}).get("total", 0)
            return f"Total revenue: ₹{total}"
        except Exception as e:
            return f"Error calculating total revenue: {str(e)}"
        
class OutstandingPaymentsTool(BaseTool):
    name: str = "outstanding_payments"
    description: str = "Get all orders with pending status and total unpaid amount"
    args_schema: Type = NoArgsSchema

    def _run(self) -> str:
        try:
            pending_orders = list(orders_collection.find({"status": "pending"}))
            for o in pending_orders:
                o["_id"] = str(o["_id"])
            total_due = sum(o["amount"] for o in pending_orders)
            return {
                "pending_orders": pending_orders,
                "total_outstanding_amount": total_due
            }
        except Exception as e:
            return f"Error fetching outstanding payments: {str(e)}"
