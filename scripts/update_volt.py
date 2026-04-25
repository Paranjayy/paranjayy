import requests
import re
import os

def update_volt():
    # Comprehensive Music Intelligence
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    }
    
    # Baseline from user snapshots
    data = {
        "plays": "67.5K", "minutes": "4227h 39", "songs": "11,463", "artists": "5,297", 
        "top_artist": "Pritam", "top_song": "Agar Tum Saath Ho",
        "m_plays": "1.3K", "m_minutes": "82h 23", "m_songs": "911"
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

        # Volt Logo (User Provided)
        logo_svg = """<g transform="scale(0.015) translate(0, 0)">
        <path d="M924 0c55.228 0 100 44.772 100 100v824c0 55.228-44.772 100-100 100H100C44.772 1024 0 979.228 0 924V100C0 44.772 44.772 0 100 0h824ZM413.505 341.879H292.73V711.85c0 6.98 1.292 13.509 3.876 19.585 2.584 6.075 6.202 11.376 10.853 15.9 4.65 4.524 10.077 8.08 16.279 10.665 6.201 2.585 12.79 3.878 19.767 3.878 40.569 0 78.23-5.494 112.985-16.482 34.754-10.988 66.925-26.113 96.511-45.374 29.587-19.261 56.59-42.142 81.008-68.643 24.419-26.5 46.512-55.328 66.28-86.482 19.767-31.154 37.273-63.924 52.519-98.31 15.245-34.386 28.552-69.289 39.922-104.71H665.753c-4.65 17.84-11.692 38.006-21.124 60.5-9.431 22.493-20.865 45.438-34.302 68.836-13.437 23.398-28.747 46.214-45.93 68.449-17.184 22.234-35.853 42.077-56.008 59.529-20.155 17.451-41.538 31.477-64.147 42.077-22.61 10.6-30.737 8.627-30.737 5.9V341.88Z" fill="#1DB954"></path>
        <path d="m2016.176 926 207.422-646.875H1972.23l-90.82 452.93h-4.687l-93.75-452.93h-258.985L1734.34 926h281.836Zm569.531 16.406c211.523 0 340.43-121.289 340.43-340.43 0-213.867-131.836-339.257-340.43-339.257-207.422 0-339.844 126.562-339.844 339.258 0 218.554 128.907 340.43 339.844 340.43Zm0-171.68c-60.352 0-96.094-59.765-96.094-168.163 0-105.47 37.5-168.165 96.094-168.165 59.18 0 96.68 62.696 96.68 168.164 0 108.399-36.914 168.165-96.68 168.165ZM3243.129 926V80.492h-240.234V926h240.234Zm406.055 0c45.703 0 76.171-4.102 99.023-8.79V750.806c-14.062 2.343-22.852 2.93-41.016 2.93-49.218 0-72.656-21.094-72.656-61.524V453.148h113.672V279.125h-113.672V137.328h-240.234v141.797h-85.547v174.023h85.547v292.383c0 127.735 72.07 180.469 254.883 180.469Zm314.062 8.203c67.383 0 121.875-54.492 121.875-121.875 0-67.383-54.492-121.875-121.875-121.875-67.383 0-121.875 54.492-121.875 121.875 0 67.383 54.492 121.875 121.875 121.875ZM4487.66 926V453.148h117.188V284.984h-124.22V269.75c0-29.297 22.852-49.219 80.274-49.219 16.407 0 33.985 1.172 45.703 3.516V80.492c-25.195-5.273-71.484-9.96-112.5-9.96-183.984 0-246.68 58.593-246.68 187.5v26.952h-85.546v168.164h85.547V926h240.234Zm431.25 0V550.414c0-56.25 29.297-91.406 77.93-91.406 51.562 0 77.93 31.055 77.93 92.578V926h227.93V550.414c0-56.836 28.71-91.406 77.343-91.406 52.148 0 78.516 30.469 78.516 91.992v375h240.234V488.89c0-131.835-86.719-222.656-212.695-222.656-98.438 0-176.953 56.836-198.633 142.383h-4.688c-15.82-90.82-81.445-142.383-179.882-142.383-88.477 0-161.133 56.25-185.157 143.555h-4.687V279.125h-234.375V926h240.234Z" fill="#F0F6FC" fill-rule="nonzero"></path>
        </g>"""

        svg_content = f"""<svg width="450" height="230" viewBox="0 0 450 230" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="450" height="230" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="449" height="229" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  
  <g transform="translate(20, 25)">
    {logo_svg}
  </g>

  <!-- Metrics Grid -->
  <g transform="translate(20, 75)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11" font-weight="bold">ALL-TIME PLAYS</text>
    <text x="0" y="22" fill="#1DB954" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="20">{data['plays']}</text>
    
    <text x="140" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11" font-weight="bold">MINUTES LISTENED</text>
    <text x="140" y="22" fill="#1DB954" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="20">{data['minutes']}</text>
    
    <text x="300" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11" font-weight="bold">LIBRARY SIZE</text>
    <text x="300" y="22" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="20">{data['songs']} <tspan fill="#8B949E" font-size="10" font-weight="normal">SONGS</tspan></text>
  </g>

  <line x1="20" y1="115" x2="430" y2="115" stroke="#2D333B" stroke-width="1" stroke-dasharray="2 2"/>

  <!-- Monthly Pulse -->
  <g transform="translate(20, 145)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11" font-weight="bold">MONTHLY PULSE (LAST 30D)</text>
    <text x="0" y="20" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['m_plays']} <tspan fill="#8B949E" font-weight="normal" font-size="10">PLAYS</tspan></text>
    <text x="140" y="20" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['m_minutes']} <tspan fill="#8B949E" font-weight="normal" font-size="10">MINS</tspan></text>
    <text x="300" y="20" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{data['m_songs']} <tspan fill="#8B949E" font-weight="normal" font-size="10">SONGS</tspan></text>
  </g>

  <!-- Top Highlights -->
  <g transform="translate(20, 195)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TOP ARTIST: <tspan fill="#1DB954" font-weight="bold">{data['top_artist']}</tspan></text>
    <text x="210" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TOP TRACK: <tspan fill="#F0F6FC" font-weight="bold">{data['top_song']}</tspan></text>
  </g>
</svg>"""

        os.makedirs("metrics", exist_ok=True)
        with open("metrics/volt-card.svg", "w") as f:
            f.write(svg_content)
        print("Volt.fm comprehensive card updated.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_volt()
