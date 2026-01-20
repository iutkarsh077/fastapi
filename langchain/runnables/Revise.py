from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

prompt = PromptTemplate(
    template="Write a roast on the topic of ${topic}",
    input_variables=["topic"]
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

parser = StrOutputParser()

chain = RunnableSequence(prompt, model, parser)

result = chain.invoke({"topic": "Software Developers"})

print(result)