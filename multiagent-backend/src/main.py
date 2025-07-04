from fastapi import FastAPI , APIRouter
from routes import support_agent , dashboard_agent
from dotenv import load_dotenv
load_dotenv()   

app = FastAPI()

#Api Versioning 
api_v1 = APIRouter(prefix = "/api/v1")

#health-check router
@app.get("/health")
async def health_check():
    return {"message " : " Health : Ok !!"}

#Include the routers 
api_v1.include_router(support_agent.router , prefix = "/support-agent", tags = ["Support Agent"])
api_v1.include_router(dashboard_agent.router , prefix = "/dashboard-agent" , tags = ["Dashboard Agent"])

#Include the versioned router 
app.include_router(api_v1)
