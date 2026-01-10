from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=100)

chatHistory = []

while True:
    user_input = input("Enter your question: ")
    answers = { "role": "user", "content": user_input }
    if user_input == "exit":
        break
    chatHistory.append(answers)
    response = model.invoke(chatHistory)
    answers2 = { "role": "assistant", "content": response.content }
    chatHistory.append(answers2)
    print(response.content)