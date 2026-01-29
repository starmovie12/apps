import os
import re
import cloudscraper
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- ADVANCED EXTRACTOR ---
def extract_link(url):
    try:
        # Browser Headers set karna taaki bot na lage
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        print(f"🔄 Connecting to: {url}")
        
        # Allow Redirects = True (Agar wo khud HubCloud par bhej de)
        response = scraper.get(url, allow_redirects=True)
        html = response.text
        
        # --- DEBUGGING (Logs check karne ke liye) ---
        # Page ka title print karenge taaki pata chale "Cloudflare" ne roka ya page khula
        page_title = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if page_title:
            print(f"📄 Page Title Found: {page_title.group(1).strip()}")
        else:
            print("⚠️ No Page Title Found")

        # --- PATTERN MATCHING ---
        
        # 1. Sabse Common: HubCloud Link (Quotes ke sath ya bina)
        # Regex explanation: Find http/https, then hubcloud/hubdrive/pixel, then any character until quote/space
        match_direct = re.search(r'(https?://(hubcloud|hubdrive|drive\.google|pixel)[a-zA-Z0-9\-\.]+(/drive/)?[^"\s\'<>]+)', html)
        if match_direct:
            print("✅ Direct Link Matched!")
            return match_direct.group(1)
            
        # 2. 'Download' Button ke andar ka link
        # Kabhi kabhi link 'HubCloud' nahi hota, bas button hota hai
        match_btn = re.search(r'href="([^"]+)"[^>]*class="[^"]*btn[^"]*"', html, re.IGNORECASE)
        if match_btn:
            link = match_btn.group(1)
            if link.startswith("http"):
                print("✅ Button Link Matched!")
                return link

        # 3. Meta Refresh (Agar page redirect kar raha ho)
        match_meta = re.search(r'content="0;url=([^"]+)"', html, re.IGNORECASE)
        if match_meta:
            print("✅ Meta Refresh Link Found!")
            return match_meta.group(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        
    return None

# --- WEBSITE UI ---
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>⚡ HubDrive Unlocker v2</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f0f0f; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1a1a1a; padding: 25px; border-radius: 12px; width: 90%; max-width: 420px; text-align: center; border: 1px solid #333; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        h2 { color: #FFD700; margin-bottom: 20px; }
        input { width: 90%; padding: 14px; margin-bottom: 20px; border: 1px solid #444; border-radius: 8px; background: #222; color: white; outline: none; font-size: 16px; }
        button { width: 100%; padding: 14px; border: none; border-radius: 8px; background: #FFD700; color: #000; font-weight: bold; cursor: pointer; font-size: 16px; }
        button:hover { background: #ffea00; }
        .result { margin-top: 25px; padding: 15px; background: #111; border-radius: 8px; border: 1px solid #FFD700; word-break: break-all; }
        a { color: #FFD700; text-decoration: none; font-weight: bold; font-size: 18px; }
        .error { color: #ff4444; background: rgba(255,68,68,0.1); padding: 10px; border-radius: 5px; margin-top: 15px; }
        .info { font-size: 12px; color: #aaa; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>⚡ HubDrive v2</h2>
        <form action="/get" method="post">
            <input type="text" name="url" placeholder="Paste HubDrive URL..." required>
            <button type="submit">Unlock Link 🔓</button>
        </form>
        
        {% if result %}
            <div class="result">
                <p>✅ <b>Success! Found:</b></p>
                <a href="{{ result }}" target="_blank">📥 Click to Download</a>
            </div>
        {% elif error %}
            <div class="error">
                ❌ <b>Link Not Found!</b><br>
                <small>Logs check karein (Render Dashboard).</small>
            </div>
        {% endif %}
        
        <p class="info">Status: Online | Bot: CloudScraper</p>
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
    print(f"🔍 User Request: {url}")
    link = extract_link(url)
    
    if link:
        return render_template_string(HTML_CODE, result=link)
    else:
        return render_template_string(HTML_CODE, error=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
