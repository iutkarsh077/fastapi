from pydantic import BaseModel
from typing import List, Optional, Dict
class UserTypes(BaseModel):
    name: str
    age: int
    weight: float
    allergy: Optional[List[str]] = None
    contact: Dict[str, str]


def UserInformation(user: UserTypes):
    # print(f"User name is {user.name} and age is {user.age}")
    print(user)
    print("User updated")


dict1 = { "name": "Utkarsh", "age": 32, "weight": 78.98, "allergy": ["Sugar", "Salt"], "contact": { "street": "129 left street", "phone": "876876872" } }
firstUser = UserTypes(**dict1)
UserInformation(firstUser)