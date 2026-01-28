import os
import re
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- BACKEND LOGIC ---
def extract_link(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        # 10 second timeout taaki server latke na
        response = requests.get(url, headers=headers, timeout=10)
        
        # Regex Pattern to find HubCloud Link
        pattern = r'href="(https?://hubcloud\.foo/drive/[^"]+)"'
        match = re.search(pattern, response.text)
        
        if match:
            return match.group(1)
    except:
        pass
    return None

# --- FRONTEND UI ---
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Link Extractor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #121212; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1e1e1e; padding: 25px; border-radius: 10px; width: 90%; max-width: 400px; text-align: center; border: 1px solid #333; }
        input { width: 90%; padding: 12px; margin-bottom: 15px; border: none; border-radius: 5px; background: #333; color: white; }
        button { width: 100%; padding: 12px; border: none; border-radius: 5px; background: #00d2ff; color: #000; font-weight: bold; cursor: pointer; }
        .result { margin-top: 20px; word-break: break-all; color: #00ff88; }
        .error { color: #ff5555; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 Live Extractor</h2>
        <form action="/get" method="post">
            <input type="text" name="url" placeholder="Paste HubDrive URL..." required>
            <button type="submit">Extract Link</button>
        </form>
        
        {% if result %}
            <div class="result">
                <p>✅ Found:</p>
                <a href="{{ result }}" target="_blank" style="color:#00ff88;">Click to Download</a>
            </div>
        {% elif error %}
            <p class="error">❌ Link Not Found</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/get', methods=['POST'])
def get_link_route():
    url = request.form.get('url')
    link = extract_link(url)
    
    if link:
        return render_template_string(HTML_CODE, result=link)
    else:
        return render_template_string(HTML_CODE, error=True)

if __name__ == '__main__':
    # Render ke liye PORT environment variable zaroori hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
