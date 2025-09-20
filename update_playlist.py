import requests
from datetime import datetime

# Source playlist dari iill.top
SOURCE_URL = "https://tv.iill.top/m3u/MyTV"

# File hasil update
OUTPUT_FILE = "HK_official.m3u"

# Custom setting
CUSTOM_LOGO = "https://raw.githubusercontent.com/tunebox-digital/icon/refs/heads/main/0000.png"
CUSTOM_GROUP = "HONGKONG"

# Mapping rasmi (contoh kecil, boleh extend semua 97)
MAPPING = {
    "翡翠台": "TVB Jade",
    "翡翠台 4K": "TVB Jade 4K",
    "明珠台": "TVB Pearl",
    "無綫新聞台": "TVB News",
    "娛樂新聞台": "TVB Entertainment News",
    "黃金翡翠台": "TVB Gold Jade",
    "千禧經典台": "TVB Classic",
    "TVB Plus": "TVB Plus",
}

def fetch_source():
    print("Downloading source playlist...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Referer": "https://tv.iill.top/"
    }
    r = requests.get(SOURCE_URL, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text.splitlines()



def apply_rules(lines):
    new_lines = ["#EXTM3U"]
    for i, line in enumerate(lines):
        if line.startswith("#EXTINF"):
            # Edit group-title & logo
            if 'group-title=' in line:
                parts = line.split('group-title=')
                left = parts[0]
                right = parts[1].split(',', 1)[1]
                line = f'{left}group-title="{CUSTOM_GROUP}",{right}'
            if 'tvg-logo=' in line:
                parts = line.split('tvg-logo=')
                left = parts[0]
                right = parts[1].split(' ', 1)[1]
                line = f'{left}tvg-logo="{CUSTOM_LOGO}" {right}'
            # Edit nama channel ikut mapping
            name = line.split(",")[-1].strip()
            if name in MAPPING:
                line = line.rsplit(",", 1)[0] + "," + MAPPING[name]
        new_lines.append(line)
    return "\n".join(new_lines)

def save_file(content):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved updated playlist → {OUTPUT_FILE}")

def main():
    lines = fetch_source()
    updated = apply_rules(lines)
    updated += f"\n# Updated on {datetime.utcnow()} UTC"
    save_file(updated)

if __name__ == "__main__":
    main()
