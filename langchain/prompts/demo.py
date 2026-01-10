from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import load_prompt

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=100)
template1 = load_prompt('template.json')

prompt = template1.invoke({"name": "Utkarsh"})
result = model.invoke(prompt)

print(result)