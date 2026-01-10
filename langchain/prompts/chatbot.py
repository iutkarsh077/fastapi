from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=100)

# chatHistory = []

messages = [
    SystemMessage("You are a assistant")
]

while True:
    user_input = input("Enter your question: ")
    if user_input == "exit":
        break
    messages.append(HumanMessage(user_input))
    response = model.invoke(messages)
    messages.append(AIMessage(response.content))
    print(response.content)