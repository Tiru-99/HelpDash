from crewai.tools import BaseTool
from typing import Type
from db.mongo import db
from datetime import datetime, timezone
from models.enquiries import Enquiries

enquiries_collection = db["enquiries"]

class CreateEnquiryTool(BaseTool):
    name: str = "create_enquiry"
    description: str = "Store a new client enquiry in the database"
    args_schema: Type = Enquiries

    # Accept arbitrary kwargs parsed by Pydantic
    def _run(self, **kwargs) -> str:
        try:
            kwargs["created_at"] = datetime.now(timezone.utc).isoformat()
            enquiries_collection.insert_one(kwargs)
            return f"✅ Enquiry submitted (ID `{kwargs['_id']}`)"
        except Exception as e:
            return f"❌ Error creating enquiry: {str(e)}"
