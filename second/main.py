import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import User
from pymongo import AsyncMongoClient

load_dotenv()
app = FastAPI()

conn = AsyncMongoClient(os.environ.get("uri"))

@app.get("/health")
def HealthCheck():
    return JSONResponse(status_code=200, content={"message": "Everything is working fine", "status": True})


@app.post("/createUser")
async def CreateUser(user: User):
    user_info = user.model_dump(exclude_unset=True)
    print("client", conn)
    result =  await conn.user_app.user.insert_one(user_info)
    
    return JSONResponse(status_code=200, content={"result": str(result.inserted_id), "status": True})