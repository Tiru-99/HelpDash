from fastapi import FastAPI , APIRouter
from fastapi.middleware.cors import CORSMiddleware
from src.routes.support_agent import router as support_router
from src.routes.dashboard_agent import router as dashboard_router
from dotenv import load_dotenv
load_dotenv()   

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Api Versioning 
api_v1 = APIRouter(prefix = "/api/v1")

#health-check router
@app.get("/health")
async def health_check():
    return {"message " : " Health : Ok !!"}

#Include the routers 
api_v1.include_router(support_router , prefix = "/support-agent", tags = ["Support Agent"])
api_v1.include_router(dashboard_router , prefix = "/dashboard-agent" , tags = ["Dashboard Agent"])

#Include the versioned router 
app.include_router(api_v1)
