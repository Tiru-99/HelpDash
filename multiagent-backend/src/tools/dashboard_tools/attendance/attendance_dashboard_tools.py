from crewai.tools import BaseTool 
from db.mongo import db
from typing import Type
from pydantic import BaseModel

attendance_collection = db["attendance"]

class NoArgsSchema(BaseModel):
    pass

class AttendancePercentageTool(BaseTool):
    name: str = "attendance_percentage"
    description: str = "Get attendance percentage by class ID"
    args_schema: Type = NoArgsSchema

    def _run(self) -> str:
        try:
            pipeline = [
                {"$group": {
                    "_id": {"class_id": "$class_id", "status": "$status"},
                    "count": {"$sum": 1}
                }}
            ]
            data = list(attendance_collection.aggregate(pipeline))
            
            class_summary = {}
            for item in data:
                cid = item["_id"]["class_id"]
                status = item["_id"]["status"]
                if cid not in class_summary:
                    class_summary[cid] = {"present": 0, "absent": 0}
                class_summary[cid][status] = item["count"]

            for cid in class_summary:
                total = class_summary[cid]["present"] + class_summary[cid]["absent"]
                class_summary[cid]["percentage"] = round(
                    (class_summary[cid]["present"] / total) * 100, 2
                ) if total > 0 else 0

            return class_summary
        except Exception as e:
            return f"Error calculating attendance %: {str(e)}"
        
class DropOffRateTool(BaseTool):
    name: str = "drop_off_rate"
    description: str = "Show how many times each client was absent"
    args_schema: Type = NoArgsSchema

    def _run(self) -> str:
        try:
            pipeline = [
                {"$match": {"status": "absent"}},
                {"$group": {"_id": "$client_id", "absent_count": {"$sum": 1}}},
                {"$sort": {"absent_count": -1}}
            ]
            result = list(attendance_collection.aggregate(pipeline))
            return result
        except Exception as e:
            return f"Error calculating drop-off rate: {str(e)}"

