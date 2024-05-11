from quart import request ,jsonify, Quart


app = Quart(__name__)
@app.post("/message")
async def message():
    data = await request.get_json()
    return {"input": data, "extra": True}



@app.get("/message")
async def message():
    return jsonify(["a", "b"])