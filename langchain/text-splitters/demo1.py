from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

# loader = TextLoader("./poem.txt", encoding="utf-8")

# data = loader.load()

myfile = ""

with open("./poem.txt", "r") as f:
    myfile = f.read()
text_splitter =  RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
texts = text_splitter.split_text(myfile.strip())

print("\n")
print("\n")
print("\n")

print(texts)