from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
import os

documents2 = [
    Document(
        page_content="The Indian Premier League (IPL) is a professional T20 cricket league in India, featuring franchise-based teams and played annually with top players from around the world.",
        metadata={"source": "https://example.com/ipl-introduction"}
    ),
    Document(
        page_content="IPL matches follow the Twenty20 format, where each team plays 20 overs, making the games fast-paced and highly entertaining for fans.",
        metadata={"source": "https://example.com/ipl-format"}
    ),
    Document(
        page_content="The IPL includes teams representing different Indian cities, and each season teams compete in a points table to qualify for the playoffs and finals.",
        metadata={"source": "https://example.com/ipl-teams"}
    ),
    Document(
        page_content="IPL auctions allow franchises to buy and build squads by selecting players based on budgets, strategy, and team requirements each season.",
        metadata={"source": "https://example.com/ipl-auction"}
    ),
    Document(
        page_content="The IPL has become one of the most popular cricket leagues globally, known for its large fan following, high-quality cricket, and major brand sponsorships.",
        metadata={"source": "https://example.com/ipl-popularity"}
    ),
]
load_dotenv()

embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

db_api_key = os.getenv('QDRANT_DB')
db_url = os.getenv('QDRANTDB_URL')


if(db_api_key == None or db_url == None):
    raise Exception("No Keys in Env")

qdrant = QdrantVectorStore.from_documents(
    documents = documents2,
    embedding = embedding,
    url = db_url,
    api_key=db_api_key,
    collection_name = "my_documents"
)

print(qdrant)