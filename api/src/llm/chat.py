import openai
from langchain_community.adapters import openai as lc_openai
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI


class Chat():
    async def chatCompletion(content, role = 'user', functionCall = None, toolCalls = None, temperature = 0):
        message = {'content': content,
                    'role': role,
                    'function_call': functionCall,
                    'tool_calls': toolCalls
                    }
        result = openai.chat.completions.create(
            messages = message, model="gpt-3.5-turbo", 
            temperature=temperature
        )
        result.choices[0].message.model_dump()
        
    async def queryGenerator():
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        chain = create_sql_query_chain(llm, db)
        response = chain.invoke({"question": "How many employees are there"})
        response