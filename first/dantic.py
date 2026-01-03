from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import List, Optional, Dict

class Address(BaseModel):
    city: str
    country: str
    street: str

class UserTypes(BaseModel):
    name: str
    age: int = Field(gt=0, default=123)
    weight: float
    email: EmailStr
    allergy: Optional[List[str]] = None
    contact: Dict[str, str]
    address: Optional[Address] = None
    
    @field_validator("email")
    @classmethod
    def EmailValidator(cls, value: str):
        print("The cls is: ", cls.getName())
        valid_domains = ["icici.com", "hdfc.com", "google.com", "bob.com"]
        getDomain = value.split("@")[-1]
        if getDomain not in valid_domains:
            raise ValueError("Invalid domain")
        
        # return value
        
        
    def getName():
        return "hey there another methode"
    
    @model_validator(mode="after")
    def HaveEmergencyNumber(cls, model):
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError("Emergency contact is not available")
        return model


def UserInformation(user: UserTypes):
    # print(f"User name is {user.name} and age is {user.age}")
    print(user)
    print("User updated")
    


dict1 = { "name": "Utkarsh", "age": 10, "weight": 78.98,  "email": "utkarshsingh@google.com", "allergy": ["Sugar", "Salt"], "contact": { "street": "129 left street", "phone": "876876872", "emergency": "79082092" } }
firstUser = UserTypes(**dict1)
UserInformation(firstUser)