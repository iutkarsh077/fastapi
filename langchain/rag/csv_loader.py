from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

load_dotenv()
loader = CSVLoader(file_path="../public/MOCK_DATA.csv")

data = loader.load()
prompt = PromptTemplate(
    template="Extract all the emails from this {topic}",
    input_variables=["topic"]
)
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

parser = StrOutputParser()


chain = RunnableSequence(prompt, model, parser)

result = chain.invoke({ "topic": data })


print(result)