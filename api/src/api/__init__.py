from quart import request ,jsonify, Quart,jsonify
import os,sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
rpath = os.path.abspath('../../../../backend')

if rpath not in sys.path:
    sys.path.insert(0, rpath)
    print(rpath)

app = Quart(__name__)
# from api.src.llm.tools import chatCompletion

load_dotenv()
llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def run() -> None:
    app.run()
    

@app.post("/getQuery")
async def userInput():
    message = await request.get_json()
    print("mesaf",message.get("query"))
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an SQL query generator. you can produce SQL queries without prior knowledge of specific table information. You will generate SQL queries based on each input provided to you, identifying words that could be a name of a table. If necessary information is missing or insufficient to generate a valid SQL query, you will return None."),
        ("user", "{input}")
    ])
    output_parser = StrOutputParser()
    chain = prompt | llm  | output_parser
    return chain.invoke({"input": "select all users and order them "})

@app.post("/echo")
async def echo():
    data =  await request.get_json()
    print(data)
    return {"input": data, "extra": True}

