import os
import re
import cloudscraper
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- SMART LINK EXTRACTOR ---
def extract_link(url):
    try:
        # CloudScraper browser banke jayega
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        print(f"Checking URL: {url}") # Logs ke liye
        response = scraper.get(url)
        
        # --- FIX: IMPROVED PATTERNS (Ab ye sab pakdega) ---
        
        # 1. HubCloud (Koi bhi extension: .space, .club, .me etc)
        # Hum dhoond rahe hain: href="https://hubcloud..."
        match = re.search(r'href="(https?://hubcloud\.[a-z]+/drive/[^"]+)"', response.text)
        if match:
            return match.group(1)
            
        # 2. Google Drive Links
        match_g = re.search(r'href="(https?://drive\.google\.com/[^"]+)"', response.text)
        if match_g:
            return match_g.group(1)

        # 3. Pixel Links (Common in HubDrive)
        match_p = re.search(r'href="(https?://pixel\.[a-z]+/[^"]+)"', response.text)
        if match_p:
            return match_p.group(1)

        # 4. Agar upar wale fail ho jayein, to 'Download' text wala link dhoondho
        # Ye 'jugaad' hai agar pattern change ho gaya ho
        match_text = re.search(r'href="([^"]+)"[^>]*>Download', response.text)
        if match_text:
             link = match_text.group(1)
             if "http" in link:
                 return link

    except Exception as e:
        print(f"Error: {e}")
        
    return None

# --- WEBSITE UI ---
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>⚡ HubDrive Unlocker</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #121212; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1e1e1e; padding: 25px; border-radius: 12px; width: 90%; max-width: 400px; text-align: center; border: 1px solid #333; }
        h2 { color: #00ff88; margin-bottom: 20px; }
        input { width: 90%; padding: 14px; margin-bottom: 20px; border: 1px solid #444; border-radius: 8px; background: #2a2a2a; color: white; outline: none; }
        button { width: 100%; padding: 14px; border: none; border-radius: 8px; background: #00ff88; color: #000; font-weight: bold; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background: #111; border: 1px solid #00ff88; border-radius: 8px; word-break: break-all; }
        a { color: #00ff88; font-weight: bold; font-size: 18px; text-decoration: none; }
        .error { color: #ff5555; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 Link Unlocker</h2>
        <form action="/get" method="post">
            <input type="text" name="url" placeholder="Paste HubDrive Link..." required>
            <button type="submit">Extract Link</button>
        </form>
        
        {% if result %}
            <div class="result">
                <p>✅ Found!</p>
                <a href="{{ result }}" target="_blank">Download Here</a>
            </div>
        {% elif error %}
            <div class="error">❌ Link Not Found inside page.</div>
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
