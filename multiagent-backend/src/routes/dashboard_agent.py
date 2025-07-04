from fastapi import APIRouter
from pydantic import BaseModel
from config.dashboard_query_engine import run_dashboard_analytics

router = APIRouter()

class PromptInput(BaseModel) :
    prompt : str


@router.post('/prompt')
async def dashboard_agent(payload : PromptInput):
    try:
        response = run_dashboard_analytics(payload.prompt)
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}