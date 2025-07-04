from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from db.mongo import db

payments_collection = db["payments"]
orders_collection = db["orders"]

class PaymentInput(BaseModel):
    order_id: str = Field(..., description="Order ID to get payment details")

class PendingDuesInput(BaseModel):
    order_id: str = Field(..., description="Order ID to calculate pending dues")


class GetPaymentByOrderTool(BaseTool):
    name: str = "get_payment_by_order"
    description: str = "Retrieve payment details for a given order ID"
    args_schema: Type = PaymentInput

    def _run(self, order_id: str):
        try:
            payment = payments_collection.find_one({"order_id": order_id})

            if not payment:
                return f"No payment found for order ID: {order_id}"

            payment["_id"] = str(payment["_id"])  # make JSON-serializable
            return payment

        except Exception as e:
            return f"Error retrieving payment info for {order_id}: {str(e)}"
        
        

class CalculatePendingDuesTool(BaseTool):
    name: str = "calculate_pending_dues"
    description: str = "Calculate any pending payment dues for a given order"
    args_schema: Type = PendingDuesInput

    def _run(self, order_id: str):
        try:
            order = orders_collection.find_one({"_id": order_id})
            payment = payments_collection.find_one({"order_id": order_id})

            if not order:
                return f"No order found with ID: {order_id}"
            if not payment:
                return f"No payment record found for order ID: {order_id}"

            total = order.get("total_amount", 0)
            paid = payment.get("amount", 0)
            pending = total - paid

            return {
                "order_id": order_id,
                "total_amount": total,
                "paid_amount": paid,
                "pending_dues": pending
            }

        except Exception as e:
            return f"Error calculating dues for {order_id}: {str(e)}"