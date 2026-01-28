import requests
import re

# --- MAIN FUNCTION ---
def get_hubcloud_link(url):
    """
    Ye function URL leta hai aur HubCloud ka direct link nikal kar deta hai.
    """
    print(f"🔄 Checking URL: {url}")
    
    try:
        # Headers zaroori hain taaki website ko lage hum browser hain
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        # Request bhejna (10 second ka timeout taaki latke nahi)
        response = requests.get(url, headers=headers, timeout=10)
        
        # Pattern match karna (Jo aapne code me diya tha)
        pattern = r'href="(https?://hubcloud\.foo/drive/[^"]+)"'
        match = re.search(pattern, response.text)
        
        if match:
            return match.group(1)
        else:
            print("⚠️ Link pattern match nahi hua.")
            return None
            
    except Exception as e:
        print(f"❌ Error aaya: {e}")
        return None

# --- USE KARNE KA TARIKA ---
if __name__ == "__main__":
    # 1. Yahan apna HubDrive link paste karein 👇
    user_url = "https://hubdrive.space/file/EXAMPLE_LINK_HERE"
    
    # 2. Function call karein
    final_link = get_hubcloud_link(user_url)
    
    # 3. Result dekhein
    if final_link:
        print(f"\n✅ SUCCESS! Extracted Link:\n{final_link}")
    else:
        print("\n❌ FAILED: Link nahi mila.")
