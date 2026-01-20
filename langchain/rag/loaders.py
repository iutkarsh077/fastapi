from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv

load_dotenv()
loader = TextLoader('./poem.txt', encoding='utf-8')

prompt = PromptTemplate(
    template="Write a summary on the topic of {topic}",
    input_variables=["topic"]
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)


parser = StrOutputParser()

docs = loader.load()

chain = RunnableSequence(prompt, model, parser)

result = chain.invoke({ "topic": docs })

print(result)