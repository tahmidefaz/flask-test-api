from flask import Flask, request, jsonify, abort
import os

consoledot_unregister_system = '''
Issue:
How to unregister/delete a system registered to console.redhat.com inventory?

Resolution:
There are multiple ways to unregister/delete a system profile from the Inventory

Procedure 1: Using insights-client command itself

# insights-client  --unregister

Procedure 2: From Red Hat Satellite 6.9 and earliar UI

* Login to Satellite webui
* Navigate to Insights -> Inventory
* Select system profiles which need to be unregistered
* Click on Actions -> Unregister

Procedure 3: Using console.redhat.com UI

* Login to console.redhat.com
* Click on Inventory
* Locate the host to be removed and click on the vertical ellipse to the end of the row then click on Delete.
* Follow any additional steps that are provided as prompted
'''

search_result = {
  "count": 1,
  "results": [
      consoledot_unregister_system
  ]
}

internal_advisor_response = {
  "count": 3,
  "recommendations": [
    {
      "system_name": "server01.example.com",
      "recommendation": "Critical vulerabilites present. Update all software packages to the latest versions and apply any available security patches to address known vulnerabilities."
    },
    {
      "system_name": "webserver2.example.com",
      "recommendation": "Web application firewall (WAF) is not configured. Install and configure a web application firewall to filter and monitor HTTP traffic, protecting against common web-based threats."
    },
    {
      "system_name": "dbhost3.example.com",
      "recommendation": "Database connections lack encryption and strong access controls. Enable encryption for database connections and enforce strong access controls and password policies to secure database access."
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

@app.route('/api/v1/internal/echo')
def echo():
  token = request.headers.get('x-token-text')
  if not token:
    return jsonify({"error": "Nothing was sent to me."}), 400
  return jsonify({"received": token})
