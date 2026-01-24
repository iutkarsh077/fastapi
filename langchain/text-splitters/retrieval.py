from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="my_documents",
    url=os.getenv("QDRANTDB_URL"),
    api_key=os.getenv("QDRANT_DB")
)


similar_docs = qdrant.similarity_search("How teams buy players in IPL?", k=2)

for doc in similar_docs:
    print(doc.page_content)
    print(doc.metadata)
    print("------")
