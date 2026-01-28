# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# from pydantic import BaseModel, Field
# from langchain.tools import tool
# from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# load_dotenv()

# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

# class Multiply_Types(BaseModel):
#     a: int = Field(description="First number")
#     b: int = Field(description="Second number")

# @tool(args_schema=Multiply_Types)
# def multiplyInput(a: int, b: int):
#     """Multiply tow numbers"""
#     return a * b

# llm = model.bind_tools([multiplyInput])
# query = HumanMessage("Please multiply 2 and 67")
# messages = [query]
# result = llm.invoke(messages)

# print(result)
# if result.tool_calls:
#     tool_call = result.tool_calls[0]
#     ans1 = result.tool_calls[0]['args']
#     output = multiplyInput.invoke(ans1)
#     tool_msg = ToolMessage(
#         content=str(output),
#         tool_call_id=tool_call["id"]
#     )

#     messages.append(tool_msg)
    
# final_answer = model.invoke(messages)
# print(final_answer)



# from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.tools import tool
# from pydantic import BaseModel, Field
# from dotenv import load_dotenv

# load_dotenv()


# class Multiply_Types(BaseModel):
#     num1: int = Field(description="First number")
#     num2: int = Field(description="Second number")

# @tool(args_schema=Multiply_Types)
# def MultiplyInput(num1: int, num2: int):
#     """Multiply num1 and num2 and return the result"""
#     return num1 * num2


# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", max_tokens=500)

# llm = model.bind_tools([MultiplyInput])

# query = "What is the multiplication of 5 and 34?"
# messages = [query]

# ans1 = llm.invoke(messages)
# print(ans1)

# if ans1.tool_calls:
#     tool_call = ans1.tool_calls[0]
#     args = tool_call['args']
#     output = MultiplyInput.invoke(args)
#     print(output)
#     tool_response = ToolMessage(
#         content=output,
#         tool_call_id=tool_call['id']
#     )
#     messages.append(tool_response)
    
# final_answer = model.invoke(messages)
# print(final_answer.content)


import asyncio
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

import httpx

load_dotenv()

# -------------------------
# Tool Schemas
# -------------------------

class AddIntegersTypes(BaseModel):
    num1: int = Field(description="First number")
    num2: int = Field(description="Second number")


# -------------------------
# Tools
# -------------------------

@tool(args_schema=AddIntegersTypes)
def AddNumbers(num1: int, num2: int) -> int:
    """Add two integers"""
    return num1 + num2


@tool
async def GetGithubUserInfo(username: str):
    """Get GitHub user information"""
    url = f"https://api.github.com/users/{username}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


# -------------------------
# LLM Setup
# -------------------------

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    max_tokens=500,
)

llm_with_tools = model.bind_tools([AddNumbers, GetGithubUserInfo])


# -------------------------
# Main Execution
# -------------------------

async def main():
    query = "Give the github information of user iutkarsh077"
    
    messages = [SystemMessage("You are a helpful agent you can add number or get some information about users on github. Answer user queries related to these topics") ,HumanMessage(content=query)]

    # 1️⃣ LLM decides which tool to call
    result = await llm_with_tools.ainvoke(messages)
    print("Initial LLM response:", result)

    # 2️⃣ Execute tool(s)
    if result.tool_calls:
        for tool_call in result.tool_calls:
            name = tool_call["name"]
            args = tool_call["args"]

            if name == "AddNumbers":
                output = AddNumbers.invoke(args)  # sync tool

            elif name == "GetGithubUserInfo":
                output = await GetGithubUserInfo.ainvoke(args)  # ✅ async tool

            else:
                continue

            messages.append(
                ToolMessage(
                    content=str(output),
                    tool_call_id=tool_call["id"],
                )
            )

        # 3️⃣ LLM receives tool output
        final_response = await model.ainvoke(messages)
        print("\nFinal Answer:")
        print(final_response.content)


# -------------------------
# Entry Point
# -------------------------

if __name__ == "__main__":
    asyncio.run(main())
