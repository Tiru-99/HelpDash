from crewai.tools import BaseTool 
from db.mongo import db
from typing import Type 
from pydantic import BaseModel

orders_collection = db["orders"]
classes_collection = db["classes"]

class NoArgsSchema(BaseModel):
    pass

class EnrollmentTrendsTool(BaseTool):
    name: str = "enrollment_trends"
    description: str = "Top course with highest enrolled students"
    args_schema: Type = NoArgsSchema

    def _run(self) -> str:
        try:
            top_courses = list(orders_collection.aggregate([
                {"$group": {"_id": "$course_id", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]))
            return top_courses
        except Exception as e:
            return f"Error fetching enrollment trends: {str(e)}"
        

class CourseCompletionRateTool(BaseTool):
    name: str = "course_completion_rate"
    description: str = "Show number of completed vs scheduled classes for each course"
    args_schema: Type = NoArgsSchema

    def _run(self) -> str:
        try:
            pipeline = [
                {"$group": {
                    "_id": {"course_id": "$course_id", "status": "$status"},
                    "count": {"$sum": 1}
                }}
            ]
            stats = list(classes_collection.aggregate(pipeline))
            return stats
        except Exception as e:
            return f"Error calculating course completion: {str(e)}"

