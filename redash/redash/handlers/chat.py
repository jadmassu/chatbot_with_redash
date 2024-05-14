from flask import request, jsonify
from redash.handlers.base import BaseResource
import os
from openai import OpenAI
import requests

VARIABLE_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=VARIABLE_KEY)


class ChatResource(BaseResource):
    def post(self):
        try:
            value = request.get_json()
            question = value.get("question")
            response = requests.post("http://192.168.1.17:5000/getQuery", json=question)
            data = response.json()

            response_data = {"answer": data.get("response")}
            return jsonify(response_data), 200
        except Exception as error:
            print(error)
            return jsonify({"error": error}), 500
