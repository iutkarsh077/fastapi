from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_community.document_loaders.firecrawl import FireCrawlLoader

load_dotenv()
loader = FireCrawlLoader(
    api_key="my-api-key", url="https://snippets-saas-production.vercel.app/", mode="scrape"
)

data = loader.load()
prompt = PromptTemplate(
    template="Crawl the web page and get all the information form it {webpageUrl}",
    input_variables=["webpageUrl"]
)
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

parser = StrOutputParser()


chain = RunnableSequence(prompt, model, parser)

result = chain.invoke({ "webpageUrl": data })


print(result)