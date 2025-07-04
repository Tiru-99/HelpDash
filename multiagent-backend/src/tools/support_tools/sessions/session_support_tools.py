from typing import Type
from crewai.tools import BaseTool
from datetime import datetime, timedelta ,timezone
from pydantic import BaseModel, Field
from db.mongo import db

sessions_collection = db["classes"]
print("The sessions collections are " , sessions_collection)

# Input Classes  

class UpcomingServicesInput(BaseModel):
    days: int = Field(7, description="Number of days ahead to list upcoming services (default: 7)")

class FilterByInstructorInput(BaseModel):
    instructor_name: str = Field(..., description="Instructor name to filter classes")

class FilterByStatusInput(BaseModel):
    status: str = Field(..., description="Class status to filter by (e.g. scheduled, completed)")
    
    
#Function Classes 

class ListUpcomingServicesTool(BaseTool):
    name: str = "list_upcoming_services"
    description: str = "List all upcoming classes or services"
    args_schema: Type = UpcomingServicesInput

    def _run(self, days: int):
        try:
            now = datetime.now(timezone.utc)
            future = now + timedelta(days=days)

            # Use the correct field name: "date"
            upcoming = list(sessions_collection.find({
                "date": {"$gte": now, "$lte": future}
            }))

            for session in upcoming:
                session["_id"] = str(session["_id"])

            return upcoming or f"No upcoming services in next {days} days"

        except Exception as e:
            import traceback
            return f"Error listing upcoming services: {str(e)}\n{traceback.format_exc()}"
        

class FilterByInstructorTool(BaseTool):
    name: str = "filter_by_instructor"
    description: str = "Filter classes by instructor name"
    args_schema: Type = FilterByInstructorInput

    def _run(self, instructor_name: str):
        try:
            classes = list(sessions_collection.find({
                "instructor": instructor_name
            }))

            for c in classes:
                c["_id"] = str(c["_id"])

            return classes or f"No classes found for instructor {instructor_name}"

        except Exception as e:
            return f"Error filtering by instructor: {str(e)}"
        
        

class FilterByStatusTool(BaseTool):
    name: str = "filter_by_status"
    description: str = "Filter classes by status"
    args_schema: Type = FilterByStatusInput

    def _run(self, status: str):
        try:
            sessions = list(sessions_collection.find({
                "status": status
            }))

            for s in sessions:
                s["_id"] = str(s["_id"])

            return sessions or f"No sessions found with status: {status}"

        except Exception as e:
            return f"Error filtering by status: {str(e)}"