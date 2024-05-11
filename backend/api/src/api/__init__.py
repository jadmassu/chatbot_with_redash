from quart import request ,jsonify, Quart,jsonify
import os,sys
from dotenv import load_dotenv

rpath = os.path.abspath('../../../../backend')

if rpath not in sys.path:
    sys.path.insert(0, rpath)
    print(rpath)

app = Quart(__name__)
from api.src.openAi import chat

load_dotenv()


def run() -> None:
    app.run()
    

@app.post("/message")
async def message():
    data = await request.get_json()
    return {"input": data, "extra": True}



@app.get("/message")
async def getMessage():
#    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
#    os.environ["OPENAI_API_KEY"] = getpass.getpass ("OPENAI_API_KEY:")
   return jsonify( await chat.message())