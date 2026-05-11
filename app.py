import os
import socket
from flask import Flask, jsonify, render_template_string, redirect, request

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))
VERSION = os.environ.get("VERSION", "1.0.0")
API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY is mandatory and must be set in the environment variables")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Status Dashboard</title></head>
<body>
    <h1>Status Dashboard</h1>
    <p>System monitoring interface.</p>
    <button onclick="fetchStatus()">Check Status</button>
    <pre id="output"></pre>
    <script>
        async function fetchStatus() {
            const res = await fetch('/api/v1/status');
            const data = await res.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status_redirect():
    return redirect('/api/v1/status', code=302)

@app.route('/api/v1/status')
def status_v1():
    return jsonify({
        "status": "ok",
        "hostname": socket.gethostname(),
        "version": VERSION
    })

@app.route('/api/v1/secret')
def secret():
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"message": "you found the secret"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
