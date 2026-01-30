from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse
import json
import requests

app = FastAPI()

@app.get("/")
def Home():
    answer = {
        "name": "Utkarsh",
        "age": 89
    }
    return JSONResponse(status_code=200, content=json.dumps(answer))

@app.get("/{username}")
def GetUser(username: str = Path(..., description="Enter the username"), age: int = Query(..., description="Age of the user")):
    print("user name is: ", username)
    print("Age is: ", type(age))
    return JSONResponse(status_code=201, content=f"The username is {username} and age is {age}")


@app.get("/github/{username}")
def GithubUserInfo(username: str = Path(..., description="Enter the github username")):
    try:
        response =  requests.get(f"https://api.github.com/users/{username}").json()
        # print(response)
        return response
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content="Internal Server error")