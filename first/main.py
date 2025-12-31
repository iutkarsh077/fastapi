from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return { "message": "This is a home page" }

@app.get("/about")
def about():
    return { "message": "This is a About page" } 

@app.get("/contact")
def contact():
    return { "message": "This is a Contact page" } 

@app.get("/greet")
def greet():
    return { "message": "Welcome to the team" } 