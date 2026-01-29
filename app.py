# ✅ VARIABLE USE KARO - EASIEST METHOD
import requests
import re

# Step 1: Variable mein URL store karo
HUBDRIVE_URL = "https://hubdrive.space/file/4189964814"

def extract_hubdrive_link(url):
    """Kisi bhi HubDrive URL se link extract karo"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        # Pattern match
        pattern = r'href="(https?://hubcloud\.foo/drive/[^"]+)"'
        match = re.search(pattern, response.text)
        
        if match:
            return match.group(1)
        return None
        
    except:
        return None

# Step 2: Function ko variable pass karo
link = extract_hubdrive_link(HUBDRIVE_URL)

if link:
    print(f"✅ Extracted: {link}")
else:
    print("❌ Link not found")

# Step 3: Agar URL change karna ho toh bas variable change karo
HUBDRIVE_URL = "https://hubdrive.space/file/2695470827"  # Yaha naya URL daalo
link2 = extract_hubdrive_link(HUBDRIVE_URL)
print(f"New URL result: {link2}")
