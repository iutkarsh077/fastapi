from pydantic import BaseModel, field_validator, EmailStr, Field
from typing import Optional, Annotated

class User(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    
    @field_validator("email")
    @classmethod
    def CheckEmail(cls, value: str):
        print("Cls is: ", cls)
        print("Value is: ", value)
        valid_domain = ["google.com", "yahoo.com", "amazon.com"]
        user_domain = value.split("@")[1]
        if user_domain not in valid_domain:
            print("Email is not valid")
            return ValueError("Not valid email")
        return value
    
    
class UpdateUser(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    email: Annotated[Optional[EmailStr], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    
    @field_validator("email")
    @classmethod
    def CheckEmail(cls, value: str):
        print("Cls is: ", cls)
        print("Value is: ", value)
        valid_domain = ["google.com", "yahoo.com", "amazon.com"]
        user_domain = value.split("@")[1]
        if user_domain not in valid_domain:
            print("Email is not valid")
            return ValueError("Not valid email")
        return value