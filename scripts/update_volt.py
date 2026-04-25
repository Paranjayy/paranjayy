import requests
import re
import os

def update_volt():
    url = "https://volt.fm/paranjay"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching Volt.fm stats from {url}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        
        # Extract numbers using specific patterns from the provided DOM
        plays = re.search(r'text-primary">([\d\.,]+K?)</div>.*?Plays</div>', html, re.S)
        minutes = re.search(r'text-primary">([\d\w\s,]+)</div>.*?Minutes</div>', html, re.S)
        songs = re.search(r'text-primary">([\d,]+)</div>.*?Songs</div>', html, re.S)
        artists = re.search(r'text-primary">([\d,]+)</div>.*?Artists</div>', html, re.S)
        albums = re.search(r'text-primary">([\d,]+)</div>.*?Albums</div>', html, re.S)
        
        # Extract Top Artist and Top Song
        top_artist = re.search(r'<span class="external-text">([^<]+)</span></a></div><span class="w-6 flex-1 shrink-0"></span><div class="mt-1.5 shrink-0"><button[^>]*><span>([^<]+)</span>', html)
        top_song = re.search(r'<a href="/track/[^"]+" class="link-plain external-text">([^<]+)</a></div><span class="text-gray-100"><a[^>]*>([^<]+)</a>', html)

        data = {
            "plays": plays.group(1).strip() if plays else "N/A",
            "minutes": minutes.group(1).strip() if minutes else "N/A",
            "songs": songs.group(1).strip() if songs else "N/A",
            "artists": artists.group(1).strip() if artists else "N/A",
            "albums": albums.group(1).strip() if albums else "N/A",
            "top_artist": top_artist.group(1).strip() if top_artist else "N/A",
            "top_artist_time": top_artist.group(2).strip() if top_artist else "N/A",
            "top_song": top_song.group(1).strip() if top_song else "N/A",
            "top_song_artist": top_song.group(2).strip() if top_song else "N/A"
        }

        print(f"Extracted Data: {data}")

        # SVG Template (High Fidelity Card)
        svg_content = f"""<svg width="400" height="200" viewBox="0 0 400 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="200" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="399" height="199" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  
  <!-- Header -->
  <text x="20" y="35" fill="#F0F6FC" font-family="Segoe UI, Ubuntu, sans-serif" font-weight="bold" font-size="18">Volt.fm Music Intelligence</text>
  <circle cx="360" cy="30" r="10" fill="#1DB954"/>
  <path d="M360 25C357.239 25 355 27.2386 355 30C355 32.7614 357.239 35 360 35C362.761 35 365 32.7614 365 30C365 27.2386 362.761 25 360 25ZM363.313 32.5516C363.159 32.7937 362.84 32.8687 362.599 32.7153C361.026 31.7513 358.98 31.5265 356.666 32.0556C356.39 32.119 356.114 31.9472 356.05 31.6716C355.987 31.396 356.159 31.1197 356.434 31.0563C358.969 30.478 361.233 30.738 362.949 31.7884C363.191 31.9423 363.267 32.2612 363.113 32.5029L363.313 32.5516Z" fill="white"/>

  <!-- Stats Grid -->
  <g transform="translate(20, 60)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">PLAYS</text>
    <text x="0" y="20" fill="#1DB954" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['plays']}</text>
    
    <text x="120" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">MINUTES</text>
    <text x="120" y="20" fill="#1DB954" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['minutes']}</text>
    
    <text x="240" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">SONGS</text>
    <text x="240" y="20" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['songs']}</text>
  </g>

  <g transform="translate(20, 110)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">ARTISTS</text>
    <text x="0" y="20" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['artists']}</text>
    
    <text x="120" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">ALBUMS</text>
    <text x="120" y="20" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['albums']}</text>
  </g>

  <!-- Top Highlights -->
  <line x1="20" y1="150" x2="380" y2="150" stroke="#2D333B" stroke-width="1"/>
  
  <g transform="translate(20, 175)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TOP ARTIST: <tspan fill="#F0F6FC" font-weight="bold">{data['top_artist']}</tspan></text>
    <text x="220" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TOP SONG: <tspan fill="#F0F6FC" font-weight="bold">{data['top_song']}</tspan></text>
  </g>
</svg>"""

        os.makedirs("metrics", exist_ok=True)
        with open("metrics/volt-card.svg", "w") as f:
            f.write(svg_content)
        print("Volt.fm card updated successfully.")

    except Exception as e:
        print(f"Error updating Volt.fm card: {e}")

if __name__ == "__main__":
    update_volt()
