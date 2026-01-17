from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableParallel, RunnableSequence, RunnableBranch, RunnablePassthrough

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

template = PromptTemplate(
    template="Write a paragraph on {topic}",
    input_variables=["topic"]
)


parser = StrOutputParser()

chain = RunnableSequence(template, model, parser)

chain_branch = RunnableBranch(
    (lambda x: len(x.split()) > 250, RunnableSequence(template, model, parser)),
    RunnablePassthrough()
)

result_chain = RunnableSequence(chain, chain_branch)

answer = result_chain.invoke({"topic": "Bhagat Singh"})

print(answer)