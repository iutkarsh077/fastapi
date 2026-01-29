from dotenv import load_dotenv
from langchain.tools import tool
from geopy.geocoders import Nominatim
from pydantic  import BaseModel, Field
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Annotated,Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from IPython.display import Image, display

import requests

load_dotenv()

class AgentState(TypedDict):
    """The state of the agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int

geolocator = Nominatim(user_agent="weather-app")

class SearchInput(BaseModel):
    location: str = Field(description="the city and state, e.g., San Francisco")
    date: str = Field(description="the forcasting date for when to get the weather format (yyyy-mm-dd)")
    
@tool( "get_weather_forecast", args_schema=SearchInput, return_direct=True)
def get_weather_forecast(location: str, date: str):
    """Retrieves the weather using Open-Meteo API for a given location (city) and a date(yyyy-mm-dd). Return a list dictionary with the time and tempurature (Celsius) for each hour."""
    location = geolocator.geocode(location)
    if location:
        try:
            response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&hourly=temperature_2m&start_date={date}&end_date={date}")
            data = response.json()
            print("Data is: ", data)
            return data
        except Exception as e:
            return {"error": str(e)}
        
tools = [get_weather_forecast]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    tempurature=1.0,
    max_retries= 2
)

model = llm.bind_tools(tools)

res = model.invoke(f"What is the weather in Berlin on {datetime.today()}")

print("Response is: ", res)

tools_by_name = { tool.name: tool for tool in tools }


def call_tool(state: AgentState):
    outputs = []
    
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=tool_result,
                name=tool_call["name"],
                tool_call_id=tool_call["id"]
            )
        )
    return { "messages": outputs }

def call_model(state: AgentState, config: RunnableConfig):
    response = model.invoke(state["messages"], config)
    return { "messages": [response] }

def should_continue(state: AgentState):
    messages = state["messages"]
    if not messages[-1].tool_calls:
        return "end"
    return "continue" 

workflow = StateGraph(AgentState)

workflow.add_node("llm", call_model)
workflow.add_node("tools", call_tool)

workflow.set_entry_point("llm")

workflow.add_conditional_edges("llm", should_continue, {
    "continue": "tools",
    "end": END
})

workflow.add_edge("tools", "llm")

graph = workflow.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

inputs = {"messages": [("user", f"What is the weather in Ludhiana on {datetime.today()}? for full day?")]}

for state in graph.stream(inputs, stream_mode="values"):
    last_message = state["messages"][-1]
    last_message.pretty_print()