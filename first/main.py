from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def loadPatients():
    with open("./patients.json") as file:
        data = json.load(file)
    return data

def getPatients(keyword, data):
    return data[keyword]

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

@app.get("/view")       
def ViewPatientsList():
    response = loadPatients()
    return response

@app.get("/patient/{patient_id}")
def OnePatient(patient_id: str = Path(...,description="It should have a patient id", example="P001")):
    data = loadPatients()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient is not available")


@app.get("/sort")
def SortPatient(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query("asc", description="Order of list should be asc or desc")):
    if sort_by not in ["height", "weight", "bmi"]:
        raise HTTPException(status_code=400, detail=f"Sort Query not following the rules")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail=f"Order is not correct")
    
    data = loadPatients()
    sortedData = True if order == "asc" else False
    result = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sortedData)
    return result