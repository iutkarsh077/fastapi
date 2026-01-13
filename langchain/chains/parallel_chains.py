from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()


notes = """
Artificial Intelligence (AI) is transforming the way people work, learn, and build technology by enabling machines to perform tasks that normally require human intelligence, such as understanding language, recognizing images, and making decisions from data. Today, AI is widely used in everyday applications like search engines, recommendation systems, customer support chatbots, and smart assistants, helping improve speed and efficiency in many industries. In software development, AI tools assist developers by generating code, finding bugs, and improving productivity, allowing engineers to focus more on building scalable and innovative products. However, AI also raises important concerns such as data privacy, bias, and job disruption, which makes responsible development and ethical usage essential for its long-term success."""

prompt1 = PromptTemplate(
    template="Write notes from the given topic {topic}",
    input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template="Ask some questions from these given notes {text}",
    input_variables=["text"]
)

prompt3 = PromptTemplate(
    template="By analysing the notes {notes}, answer the questions {questions}",
    input_variables=["notes", "questions"]
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

output = StrOutputParser()

parallel_chain = RunnableParallel(
   {
        "notes": prompt1 | model | output,
    "questions": prompt2 | model |output
   }
)

conclusion_chain = prompt3 | model | output

chain = parallel_chain | conclusion_chain

result = chain.invoke({ "topic": notes, "text": notes })

print(result)

chain.get_graph().print_ascii()