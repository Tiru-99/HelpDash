from fastapi import APIRouter 
from config.support_query_engine import run_support_query
from pydantic import BaseModel

class PromptInput(BaseModel) :
    prompt : str

router = APIRouter()

@router.post('/prompt')
async def support_agent(payload : PromptInput):
    try:
        response = run_support_query(payload.prompt)
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}