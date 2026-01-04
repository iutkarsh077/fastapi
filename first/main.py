from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
from fastapi.responses import JSONResponse
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Id of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient", examples=['Utkarsh'])]
    city: Annotated[str, Field(..., description="Name of city", examples=['Ludhiana'])]
    age: Annotated[int, Field(..., description="Age of the patient", examples=[21])]
    gender: Annotated[Literal["Male", "Female"], Field(..., description="Gender of the patient", examples=['Male'])]
    height: Annotated[float, Field(..., description="Height of the patient in cm", examples=[21.2])]
    weight: Annotated[float, Field(..., description="Weight of the patient in kg", examples=[89.2])]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height ** 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        
        elif self.bmi >= 18.5 and self.bmi <= 25:
            return "Normal"
        
        else:
            return "Overweight"
        
        
class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(description="Name of the patient", examples=['Utkarsh'], default=None)]
    city: Annotated[Optional[str], Field(description="Name of city", examples=['Ludhiana'], default=None)]
    age: Annotated[Optional[int], Field(description="Age of the patient", examples=[21], default=None)]
    gender: Annotated[Optional[Literal["Male", "Female"]], Field(description="Gender of the patient", examples=['Male'], default=None)]
    height: Annotated[Optional[float], Field(description="Height of the patient in cm", examples=[21.2], default=None)]
    weight: Annotated[Optional[float], Field(description="Weight of the patient in kg", examples=[89.2], default=None)]

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

def loadPatients():
    with open("./patients.json") as file:
        data = json.load(file)
    return data


def saveData(data):
    with open("./patients.json", 'w') as file:
        json.dump(data, file)

@app.post("/create")
def CreatePatient(patient: Patient):
    data = loadPatients()
    
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient id is invalid")
    
    data[patient.id] = patient.model_dump(exclude=["id"])
    saveData(data)
    
    return JSONResponse(status_code=200, content={'message': "Patient created succcessfully"})


@app.put("/update-patient/{patient_id}")
def UpdatePatientInfo(update_info: UpdatePatient, patient_id: str = Path(..., description="Id of the Patient", examples=["P001"])):
    data = loadPatients()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient id not found")
    
    print("Before Unset data is: ", update_info)
    updated_patient_info = update_info.model_dump(exclude_unset=True)
    print("After Unset data is: ", updated_patient_info)
    
    existingPatient = data[patient_id]
    
    for key, value in updated_patient_info.items():
        existingPatient[key] = value
        
    existingPatient["id"] = patient_id
    patient_pydantic = Patient(**existingPatient)
    
    data[patient_id] = patient_pydantic.model_dump(exclude=["id"])
    
    saveData(data)
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.delete("/delete-patient/${patient_id}")
def DeletePatientInfo(patient_id: str = Path(..., description="Id of the Patient", examples=["P001"])):
    data = loadPatients()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    
    saveData(data)
    
    return JSONResponse(status_code=200, content={"message": "Patient Information deleted succssfully!"})