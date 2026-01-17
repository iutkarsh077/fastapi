from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableParallel, RunnableSequence

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

template = PromptTemplate(
    template="Write a joke on {topic}",
    input_variables=["topic"]
)


parser = StrOutputParser()

chain = RunnableParallel({
    "tweet": RunnableSequence(template, model, parser),
    "linkedin": RunnableSequence(template, model, parser)
})

result = chain.invoke({ "topic": "AI" })

print(result)