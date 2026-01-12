from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()



userReview = """The Logitech MX Master 3S is a premium wireless mouse designed for professionals who prioritize comfort and productivity in daily computing tasks. It features an ergonomic, well-contoured design that fits naturally in the hand, significantly reducing wrist strain during long working hours. The mouse delivers excellent performance with its high-precision sensor, which works smoothly on most surfaces, including glass, and ensures accurate cursor control. One of its standout features is the MagSpeed scroll wheel, which allows both ultra-fast scrolling through lengthy documents and precise line-by-line navigation. Additionally, the mouse offers seamless multi-device connectivity and extensive customization through Logitech’s software, making it ideal for developers, designers, and office professionals. Although priced higher than standard wireless mice, its build quality, long battery life, and productivity-focused features make it a reliable and worthwhile investment for serious users."""


class Review(TypedDict):
    summary: str
    benefits: str
    satisfied: str
    
    
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=200)
structuredOutput = model.with_structured_output(Review)

result = structuredOutput.invoke(userReview)

print(result)