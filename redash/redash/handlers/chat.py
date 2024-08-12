from flask import request, jsonify
from redash.handlers.base import BaseResource
import os
from openai import OpenAI
import requests
import json
import time

VARIABLE_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=VARIABLE_KEY)

HOST = os.environ.get("REDASH_HOST")

api_key = os.environ.get("api_key")
backend_uri = os.environ.get("BACKEND_API_URI")


class ChatResource(BaseResource):
    def post(self):
        try:
            value = request.get_json()
            question = value.get("question")
            response = requests.post(backend_uri + "getQuery", json=question)
            data = response.json()
            response_data = {"answer": data}

            return jsonify(response_data), 200
        except Exception as error:
            print(error)
            return jsonify({"error": error}), 500


def create_query(sql_query, name):
    try:
        # Set up the headers
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        }
        data_source_id = get_data_source_id_by_name("telecom")
        query_payload = {
            "query": sql_query,
            "data_source_id": data_source_id,
            "name": name,
        }

        create_query_url = f"{HOST}/api/queries"
        response = requests.post(
            create_query_url, headers=headers, data=json.dumps(query_payload)
        )
        response.raise_for_status()
        new_query = response.json()
        query_id = new_query["id"]
        print(f"New query created with ID: {query_id}")
        return query_id

    except requests.exceptions.RequestException as e:
        print(f"Error creating query: {e}")
        return None


def execute_query(query_id):
    try:
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        }
        execute_query_url = f"{HOST}/api/queries/{query_id}/results"
        response = requests.post(execute_query_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        job = response.json()
        job_id = job["job"]["id"]
        print(f"Query execution started with Job ID: {job_id}")

        result_url = f"{HOST}/api/jobs/{job_id}"
        while True:
            status_response = requests.get(result_url, headers=headers)
            status_response.raise_for_status()
            job_status = status_response.json()

            if job_status["job"]["status"] == 3:
                query_result_id = job_status["job"]["query_result_id"]
                break
            elif job_status["job"]["status"] == 4:
                print("Query execution failed")
                return None
            else:
                print("Query still running...")
                time.sleep(5)

        results_url = f"{HOST}/api/query_results/{query_result_id}.json"
        results_response = requests.get(results_url, headers=headers)
        results_response.raise_for_status()  # Raise an HTTPError for bad responses

        results = results_response.json()
        rows = results["query_result"]["data"]["rows"]
        return rows

    except requests.exceptions.RequestException as e:
        print(f"Error executing query: {e}")
        return None


def get_data_source_id_by_name(data_source_name):
    try:
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        }
        data_sources_url = f"{HOST}/api/data_sources"
        response = requests.get(data_sources_url, headers=headers)
        response.raise_for_status()
        data_sources = response.json()
        for ds in data_sources:
            if ds["name"] == data_source_name:
                return ds["id"]
        print(f"Data source '{data_source_name}' not found.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error listing data sources: {e}")
        return None
