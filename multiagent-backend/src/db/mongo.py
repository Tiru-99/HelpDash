import os 
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_CONNECTION_URL")
DB_NAME = os.getenv("MONGO_DB_NAME")  


try:
    #connect to mongo 
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
except Exception as e:
    print(" Failed to connect to MongoDB:", e)
    db = None  # optionally fail gracefully

