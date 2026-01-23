from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from langchain.tools import tool
from typing import Annotated
import requests
load_dotenv()

# search = DuckDuckGoSearchRun()
# result = search.invoke("what is the tempurature of ludhiana for 22 january 2026?")

class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str

    
@tool(args_schema=WeatherInput, description="Tells the weather of the app")
def WeatherPredictor(location: str):
    search = DuckDuckGoSearchRun()
    result = search.invoke(f"what is the tempurature of {location} for 22 january 2026?")
    return result

@tool(description="Add two numbers")
def AddTwoNumbers(num1: int, num2: int):
    return num1 + num2


@tool(description="Information about the Github users")
async def GithubUserInformation(username: str):
    """Get the information of the user , username will be passes as parameter"""
    response = await requests.get(f"https://api.github.com/users/{username}").json()
    return response

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

agent = create_agent(
    model,
    tools=[GithubUserInformation],
    system_prompt="You are a weather forecast assistant and a mathematician. you also have information about Github users where you can make api calls to Github backend and get the relevent information about the user."
)


parser = StrOutputParser()

# chain = RunnableSequence(agent, parser)

result = agent.invoke({"messages": [{ "role": "user", "content": "Github username iutkarsh077" }]})
print(result)