# from langchain_community.tools import DuckDuckGoSearchRun
# search = DuckDuckGoSearchRun()
# result = search.invoke("Today latest news about AI")
# print(result)


# from langchain.tools import tool

# @tool
# def multiply_tool(a: int, b: int):
#     """Multiplication of two numbers"""
#     return a * b

# result = multiply_tool.invoke({'a': 8, 'b': 3})
# print(result)


from pydantic import BaseModel, Field
from typing import Literal, Annotated
from langchain.tools import tool

class Weather_Input(BaseModel):
    location: str = Field(description="City name or coordinates")
    units: Literal["Celsius", "fahrenheit"]  = Field(
        default="fahrenheit",
        description="Tempurature unit preference"
    )
    include_forecast: bool = Field(..., description="Include 5-day forecast")
    
    
@tool(args_schema=Weather_Input)
def get_weather(location: str, units: str, include_forecast: bool)-> str:
    """Get the current weather and optional forecast"""
    return f"Tempurature of {location} is 56 {units} for next 5 days"

result = get_weather.invoke({ "location": "New york City", "units": "Celsius", "include_forecast": True  })
print(result)