from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
prompt = PromptTemplate(
    template="Write five lines on {topic}",
    input_variables=["topic"]
)


prompt2 = PromptTemplate(
    template="Summarize the text in 20 words {text}",
    input_variables=["text"]
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

output = StrOutputParser()

chain = prompt | model | output | prompt2 | model | output

result = chain.invoke({ "topic": "My Best friend" })

print(result)