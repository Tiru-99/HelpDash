from crewai.tools import BaseTool 
from typing import Optional
from pydantic import BaseModel 
from db.mongo import db
from typing import Type
from datetime import datetime , timezone

clients_collection = db["clients"]

class NoArgsSchema(BaseModel):
    pass

class ClientStatusCountTool(BaseTool):
    name: str = "client_status_count"
    description: str = "Count number of active vs inactive clients"
    args_schema: Type = NoArgsSchema

    def _run(self) -> str:
        try:
            pipeline = [
                {"$group": {"_id": "$status", "count": {"$sum": 1}}}
            ]
            results = list(clients_collection.aggregate(pipeline))
            return results
        except Exception as e:
            return f"Error getting client status stats: {str(e)}"
        
class BirthdayReminderTool(BaseTool):
    name: str = "birthday_reminders"                            
    description: str = "List clients whose birthday is today"       
    args_schema: Optional[Type[BaseModel]] = NoArgsSchema       

    def _run(self) -> str:
        try:
            today = datetime.now(timezone.utc)
            mm_dd = today.strftime("-%m-%d$")# regex for '-MM-DD'
            results = list(
                clients_collection.find({"birthday": {"$regex": mm_dd, "$options": "i"}})
            )
            for r in results:
                r["_id"] = str(r["_id"])
            return results or "No birthdays today!"
        except Exception as e:
            return f"Error fetching birthday reminders: {str(e)}"
        
class NewClientsThisMonthTool(BaseTool):
    name: str = "new_clients_this_month"
    description: str = "List clients who joined this month"
    args_schema: Type = NoArgsSchema

    def _run(self) -> str:
        try:
            now = datetime.utcnow()
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            results = list(clients_collection.find({"created_at": {"$gte": first_day}}))
            for r in results:
                r["_id"] = str(r["_id"])
            return results or "No new clients this month"
        except Exception as e:
            return f"Error fetching new clients: {str(e)}"

