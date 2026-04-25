import requests
import re
import os

def update_volt():
    # We fetch All-Time and Monthly pulse
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    }
    
    data = {
        "plays": "67.5K", "minutes": "4227h 39", "songs": "11,463", "artists": "5,297", "albums": "6,698",
        "m_plays": "1.3K", "m_minutes": "82h 23", "m_songs": "911", "m_artists": "651"
    }

    try:
        # Scrape All-Time
        res = requests.get("https://volt.fm/paranjay", headers=headers)
        if res.status_code == 200:
            html = res.text
            p = re.search(r'text-primary">([\d\.,]+K?)</div>.*?Plays</div>', html, re.S)
            m = re.search(r'text-primary">([\d\w\s,]+)</div>.*?Minutes</div>', html, re.S)
            s = re.search(r'text-primary">([\d,]+)</div>.*?Songs</div>', html, re.S)
            if p: data["plays"] = p.group(1).strip()
            if m: data["minutes"] = m.group(1).strip()
            if s: data["songs"] = s.group(1).strip()

        # Scrape Monthly
        res_m = requests.get("https://volt.fm/paranjay?time_frame=last-30-d", headers=headers)
        if res_m.status_code == 200:
            html_m = res_m.text
            mp = re.search(r'text-primary">([\d\.,]+K?)</div>.*?Plays</div>', html_m, re.S)
            mm = re.search(r'text-primary">([\d\w\s,]+)</div>.*?Minutes</div>', html_m, re.S)
            ms = re.search(r'text-primary">([\d,]+)</div>.*?Songs</div>', html_m, re.S)
            if mp: data["m_plays"] = mp.group(1).strip()
            if mm: data["m_minutes"] = mm.group(1).strip()
            if ms: data["m_songs"] = ms.group(1).strip()

        svg_content = f"""<svg width="400" height="200" viewBox="0 0 400 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="200" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="399" height="199" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  
  <text x="20" y="35" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">Volt.fm Music Profile</text>

  <!-- ALL-TIME STATS -->
  <g transform="translate(20, 65)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11" font-weight="bold">ALL-TIME</text>
    <text x="0" y="22" fill="#1DB954" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['plays']} <tspan fill="#8B949E" font-weight="normal" font-size="10">PLAYS</tspan></text>
    <text x="120" y="22" fill="#1DB954" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['minutes']} <tspan fill="#8B949E" font-weight="normal" font-size="10">MINS</tspan></text>
    <text x="240" y="22" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['songs']} <tspan fill="#8B949E" font-weight="normal" font-size="10">SONGS</tspan></text>
  </g>

  <line x1="20" y1="110" x2="380" y2="110" stroke="#2D333B" stroke-width="1" stroke-dasharray="2 2"/>

  <!-- MONTHLY PULSE -->
  <g transform="translate(20, 145)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11" font-weight="bold">MONTHLY PULSE (LAST 30D)</text>
    <text x="0" y="22" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['m_plays']} <tspan fill="#8B949E" font-weight="normal" font-size="10">PLAYS</tspan></text>
    <text x="120" y="22" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['m_minutes']} <tspan fill="#8B949E" font-weight="normal" font-size="10">MINS</tspan></text>
    <text x="240" y="22" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['m_songs']} <tspan fill="#8B949E" font-weight="normal" font-size="10">SONGS</tspan></text>
  </g>
</svg>"""

        os.makedirs("metrics", exist_ok=True)
        with open("metrics/volt-card.svg", "w") as f:
            f.write(svg_content)
        print("Volt.fm unified card updated.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_volt()
