import requests
import re
import os

def update_volt():
    # Fetch data for All-Time and Last 30 Days
    url_all = "https://volt.fm/paranjay"
    url_month = "https://volt.fm/paranjay?time_frame=last-30-d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    }
    
    print(f"Syncing Volt.fm Music Profile...")
    data = {
        "plays": "67.5K", "minutes": "4227h 39", "songs": "11,463", "artists": "5,297", "albums": "6,698",
        "top_artist": "Pritam", "top_song": "Agar Tum Saath Ho",
        "m_plays": "1.3K", "m_minutes": "82h 23", "m_songs": "911", "m_artists": "651"
    }

    try:
        res_all = requests.get(url_all, headers=headers)
        if res_all.status_code == 200:
            html = res_all.text
            plays = re.search(r'text-primary">([\d\.,]+K?)</div>.*?Plays</div>', html, re.S)
            minutes = re.search(r'text-primary">([\d\w\s,]+)</div>.*?Minutes</div>', html, re.S)
            songs = re.search(r'text-primary">([\d,]+)</div>.*?Songs</div>', html, re.S)
            artists = re.search(r'text-primary">([\d,]+)</div>.*?Artists</div>', html, re.S)
            if plays: data["plays"] = plays.group(1).strip()
            if minutes: data["minutes"] = minutes.group(1).strip()
            if songs: data["songs"] = songs.group(1).strip()
            if artists: data["artists"] = artists.group(1).strip()

        res_month = requests.get(url_month, headers=headers)
        if res_month.status_code == 200:
            html_m = res_month.text
            mp = re.search(r'text-primary">([\d\.,]+K?)</div>.*?Plays</div>', html_m, re.S)
            mm = re.search(r'text-primary">([\d\w\s,]+)</div>.*?Minutes</div>', html_m, re.S)
            ms = re.search(r'text-primary">([\d,]+)</div>.*?Songs</div>', html_m, re.S)
            ma = re.search(r'text-primary">([\d,]+)</div>.*?Artists</div>', html_m, re.S)
            if mp: data["m_plays"] = mp.group(1).strip()
            if mm: data["m_minutes"] = mm.group(1).strip()
            if ms: data["m_songs"] = ms.group(1).strip()
            if ma: data["m_artists"] = ma.group(1).strip()

        os.makedirs("metrics", exist_ok=True)

        # 1. All-Time SVG
        svg_all = f"""<svg width="400" height="120" viewBox="0 0 400 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="120" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="399" height="119" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  <text x="20" y="35" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">Volt.fm - All Time</text>
  <g transform="translate(20, 70)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">PLAYS</text>
    <text x="0" y="20" fill="#1DB954" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['plays']}</text>
    <text x="120" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">MINUTES</text>
    <text x="120" y="20" fill="#1DB954" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['minutes']}</text>
    <text x="240" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">SONGS</text>
    <text x="240" y="20" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['songs']}</text>
  </g>
</svg>"""

        # 2. Monthly SVG
        svg_month = f"""<svg width="400" height="120" viewBox="0 0 400 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="120" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="399" height="119" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  <text x="20" y="35" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">Volt.fm - Last 30 Days</text>
  <g transform="translate(20, 70)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">PLAYS</text>
    <text x="0" y="20" fill="#1DB954" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['m_plays']}</text>
    <text x="120" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">MINUTES</text>
    <text x="120" y="20" fill="#1DB954" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['m_minutes']}</text>
    <text x="240" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">ARTISTS</text>
    <text x="240" y="20" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['m_artists']}</text>
  </g>
</svg>"""

        with open("metrics/volt-alltime.svg", "w") as f: f.write(svg_all)
        with open("metrics/volt-monthly.svg", "w") as f: f.write(svg_month)
        print("Volt.fm SVGs generated (Tab-ready).")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_volt()
