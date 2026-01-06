import os
from dotenv import load_dotenv
from fastapi import FastAPI, Path, HTTPException, Query, Response, Cookie, Header, Request
import json
from fastapi.responses import JSONResponse
from models import User, UpdateUser
from pymongo import AsyncMongoClient

load_dotenv()
app = FastAPI()

conn = AsyncMongoClient(os.environ.get("uri"))


@app.middleware("http")
async def MyMiddleware(request: Request, call_next):
    print("Before: ", request)
    response = await call_next(request)
    
    response.status_code = 501
    
    print("After: ", response.status_code)
    
    return response

@app.get("/health")
def HealthCheck():
    return JSONResponse(status_code=200, content={"message": "Everything is working fine", "status": True})


@app.post("/createUser")
async def CreateUser(user: User):
    user_info = user.model_dump(exclude_unset=True)
    # print("client", conn)
    result =  await conn.user_app.user.insert_one(user_info)
    return JSONResponse(status_code=200, content={"result": str(result.inserted_id), "status": True})


@app.get("/user-info/{email}")
async def getUserDetails(email: str = Path(..., description="User email id", examples=["user@gmail.com"])):
    try:
        userInfo = await conn.user_app.user.find_one({"email" :email})
        
        if not userInfo:
            raise HTTPException(status_code=404, detail="User not found")
        
        userInfo["_id"] = str(userInfo["_id"])
        return userInfo
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": e})
    
    
@app.put("/update-user/{email}")
async def UpdateUserDetails(user: UpdateUser, email: str = Path(..., description="User email id", examples=["user@gmail.com"])):
    print("User is: ", user)
    new_data = user.model_dump(exclude_unset=True)
    print("New data: ", new_data)
    try:
        result = await conn.user_app.user.find_one_and_update({'email': email}, {'$set': new_data}, return_document=True)
        
        result["_id"] = str(result["_id"])
        return JSONResponse(status_code=200, content={"data": result})
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": e})
    
    
@app.delete("/delete-user")
async def DeleteUser(email: str = Query(..., description="User email to delete", examples=["user@gmail.com"])):
    try:
        result = await conn.user_app.user.find_one_and_delete({"email": email})
        print("Result is: ", result)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
    
        return JSONResponse(status_code=200, content={"message": "User delete successfully"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server error")
    
@app.get("/set-cookie")
def SetMyCookie(response: Response, utkarsh: str = Cookie(default=None)):
    response.set_cookie(
        key="utkarsh",
        value="my-cookie",
        max_age=60 * 60,
        samesite="lax",
        httponly=True,
        secure=True
    )
    
    print("Cookie data is: ", utkarsh)
    return {"message": "Cookie has been set"}


@app.delete("/delete-cookie")
def DeleteCookie(response: Response):
    response = JSONResponse(status_code=200, content={"message": "Cookie is deleted successfully"})
    response.delete_cookie("utkarsh")
    
    return response


@app.get("/headers")
def getHeaders(request: Request, response: Response, user_agent: str = Header(default=None)):
    response = JSONResponse(status_code=200, content={"message": "Got headers"})
    
    # print("Cookies are: ", request._cookies)
    print("headers are: ", dict(request.headers))
    
    return response


