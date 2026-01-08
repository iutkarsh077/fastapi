import os
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

text = "I am utkarsh"

query_result = embeddings.embed_query(text)
print(query_result)
