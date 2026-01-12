from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

app = FastAPI()

models = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    max_tokens=500,
    max_tries = 2
)

messages = [
    SystemMessage("You are an AI Assistant your name is Utkarsh,always Respond user to english")
]

@app.get("/chat")
async def Chat(question: str = Query(..., examples=["What is your name?"])):
    messages.append(HumanMessage(question))
    model =  models.invoke(messages)
    messages.append(AIMessage(model.content))
    print(messages)
    return JSONResponse(status_code=200, content=model.content)