from langchain.agents import tool
import openai

# from langchain_community.adapters import openai as lc_openai


@tool
async def chatCompletion(
    content, role="user", functionCall=None, toolCalls=None, temperature=0
):
    message = {
        "content": content,
        "role": role,
        "function_call": functionCall,
        "tool_calls": toolCalls,
    }
    result = openai.chat.completions.create(
        messages=message, model="gpt-3.5-turbo", temperature=temperature
    )
    return result.choices[0].message.model_dump()
