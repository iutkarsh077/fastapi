from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=200)

template1 = PromptTemplate(
    template="Give me the summary of the {topic}",
    input_variables=['topic']
)

# prompt = template1.invoke({"topic": "Black hole"})
# answer = model.invoke(prompt)
parser = StrOutputParser()
chain = template1 | model | parser

result = chain.invoke({ "topic": "Black hole" })

print(result)