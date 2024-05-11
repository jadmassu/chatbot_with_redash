from quart import request ,jsonify, Quart,jsonify
import os,sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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
    

@app.post("/getUserInput")
async def userInput():
    # return True
   prompt = ChatPromptTemplate.from_messages([
    ("system", "You are sql query generator."),
    ("user", "{input}")
])
   output_parser = StrOutputParser()
   chain = prompt | llm  | output_parser
   return chain.invoke({"input": "select all the users"})



