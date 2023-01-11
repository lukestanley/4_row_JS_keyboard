from flask import Flask, jsonify, request, send_from_directory
import requests
import os

app = Flask(__name__)

# IP and port of the target server
TARGET_URL = "http://192.168.8.129:7777"

@app.after_request
def after_request(response):
    """Add headers to enable CORS"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/proxy/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@app.route('/proxy/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    """Proxy requests to the target server"""
    query_string = request.query_string.decode()
    url = f"{TARGET_URL}/{path}?{query_string}"
    print(url)
    try:
        json = request.json
    except:
        json_body = None
    try:
        resp = getattr(requests, request.method.lower())(url)
    except AttributeError:
        resp = jsonify({'message': 'Unsupported method'})
    # Forward the response headers and status code from the target server
    headers = {key: value for (key, value) in resp.headers.items()}
    return (resp.content, resp.status_code, headers)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    print("path:",path)
    if not os.path.exists(app.static_folder + '/' + path):
        # this will return 404 if file not exists
        return "file not exist", 404
    return send_from_directory(app.static_folder, path)
app.run(debug=True,host='0.0.0.0')
"""
fetch('http://localhost:5000/path-to-target-resource', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
  .then(response => response.json())
  .then(data => {
    // Do something with the data
  })
  .catch(error => {
    console.error('Error:', error);
  });
"""
