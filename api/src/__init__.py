from quart import request, jsonify, Quart
import os, sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from quart_cors import cors

rpath = os.path.abspath("../../../../backend")

if rpath not in sys.path:
    sys.path.insert(0, rpath)
    print(rpath)

app = Quart(__name__)
# from api.src.llm.tools import chatCompletion
app = cors(app, allow_origin="*")

load_dotenv()
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run() -> None:
    # app.run()
    app.run(host="0.0.0.0", port=5000)


@app.post("/getQuery")
async def userInput():
    userInput = await request.get_json()

    # message = userInput.get("question")
    print("mesaf", userInput)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an SQL query generator. You can produce SQL queries without prior knowledge of specific table information. You will generate SQL queries based on each input provided to you, identifying words that could be the name of a table. If necessary information is missing or insufficient to generate a valid SQL query, you will return None. Your response should be in the format as an object containing  query  with its query  columns with an array of columns and rows with rows of columns.",
            ),
            ("user", "{input}"),
        ]
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    response = chain.invoke({"input": userInput})
    print("RES---", response)
    return {"response": response}


@app.post("/echo")
async def echo():
    data = await request.get_json()
    print(data)
    return {"input": data, "extra": True}
