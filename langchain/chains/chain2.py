from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

template1 = PromptTemplate(
    template="Write a joke on {topic}",
    input_variables=["topic"]
)
 
parser = StrOutputParser()
chain = template1 | model | parser

result = chain.invoke({ "topic": "Best friend" })


print(result)