from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

@app.get("/")
def Home():
    return { "message": "All good and working", "status": True }

@app.get("/about")
def About():
    return { "message": "This is a aboout page", "status": True }


@app.get("/contact/{username}")
def Contact(username: str = Path(..., description="Enter your username", example="iutkarsh077")):
    if(not username):
        return HTTPException(detail="Username not provided", status_code=429)
    return {"message": f"Good evening {username}", "status": True}

@app.get("/question")
def MyQuestions(question: str = Query(..., description="Enter any question you want", example="eg: What is a dinasour?")):
    return { "message": f"{question}", "status": True }