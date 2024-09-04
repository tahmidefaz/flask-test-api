from flask import Flask, request, jsonify, abort
import os

search_result = {
  "count": 3,
  "results": [
    "hello",
    "world"
  ]
}

internal_advisor_response = {
  "count": 1,
  "recommendations": [
    {
      "system_name": "host1",
      "recommendation": "Advisor recommends a fix."
    }
  ]
}

app = Flask(__name__)

API_KEY = os.getenv('API_KEY', 'testkey')

@app.before_request
def autheticate():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        abort(401, description="Unauthorized: Invalid API Key")

@app.route('/api/v1/search')
def search():
    query = request.args.get('search_query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    return jsonify(search_result)

@app.route('/api/v1/internal/advisor')
def internal_advisor():
    return jsonify(internal_advisor_response)
