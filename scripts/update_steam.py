import requests
import os

def update_steam():
    print(f"Syncing Steam Intelligence...")
    
    # Steam data mockup based on user screenshot
    # In reality, this would use the Steam API
    games = [
        {"name": "Red Dead Redemption 2", "playtime": "188 hours", "color": "#CC0000"},
        {"name": "Grand Theft Auto V", "playtime": "59 hours", "color": "#51B135"},
        {"name": "Balatro", "playtime": "14 hours", "color": "#0078D7"}
    ]

    svg_content = f"""<svg width="450" height="200" viewBox="0 0 450 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="450" height="200" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="449" height="199" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  
  <g transform="translate(20, 20)">
    <!-- Steam Logo -->
    <path d="M15 0C6.716 0 0 6.716 0 15C0 21.05 3.593 26.255 8.718 28.795L12.39 23.473C12.188 22.955 12.073 22.385 12.073 21.785C12.073 19.347 14.048 17.373 16.486 17.373C17.067 17.373 17.621 17.487 18.125 17.685L21.728 12.457C21.657 12.227 21.619 11.983 21.619 11.731C21.619 9.387 23.518 7.488 25.862 7.488C28.206 7.488 30.105 9.387 30.105 11.731C30.105 14.075 28.206 15.974 25.862 15.974C25.594 15.974 25.333 15.948 25.084 15.898L21.465 21.144C21.637 21.666 21.732 22.226 21.732 22.808C21.732 25.688 19.396 28.024 16.516 28.024C14.045 28.024 11.968 26.297 11.411 23.989L7.545 29.588C9.824 30.505 12.339 31 15 31C23.284 31 30 24.284 30 16C30 7.716 23.284 0 15 0Z" fill="#1B2838"/>
    <path d="M15 0C6.716 0 0 6.716 0 15C0 21.05 3.593 26.255 8.718 28.795L12.39 23.473C12.188 22.955 12.073 22.385 12.073 21.785C12.073 19.347 14.048 17.373 16.486 17.373C17.067 17.373 17.621 17.487 18.125 17.685L21.728 12.457C21.657 12.227 21.619 11.983 21.619 11.731C21.619 9.387 23.518 7.488 25.862 7.488C28.206 7.488 30.105 9.387 30.105 11.731C30.105 14.075 28.206 15.974 25.862 15.974C25.594 15.974 25.333 15.948 25.084 15.898L21.465 21.144C21.637 21.666 21.732 22.226 21.732 22.808C21.732 25.688 19.396 28.024 16.516 28.024C14.045 28.024 11.968 26.297 11.411 23.989L7.545 29.588C9.824 30.505 12.339 31 15 31C23.284 31 30 24.284 30 16C30 7.716 23.284 0 15 0Z" fill="url(#steam-grad)"/>
    <defs>
      <linearGradient id="steam-grad" x1="0" y1="0" x2="30" y2="31" gradientUnits="userSpaceOnUse">
        <stop stop-color="#111D2E"/>
        <stop offset="1" stop-color="#2A475E"/>
      </linearGradient>
    </defs>
    <text x="40" y="22" fill="#66C0F4" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">Steam Pulse</text>
  </g>

  <!-- Most Played Titles -->
  <g transform="translate(20, 70)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">RECENTLY PLAYED &amp; HIGHLIGHTS</text>
    
    <!-- Game 1 -->
    <rect x="0" y="15" width="410" height="30" rx="4" fill="#1C2128"/>
    <rect x="0" y="15" width="4" height="30" rx="2" fill="{games[0]['color']}"/>
    <text x="15" y="34" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="14">{games[0]['name']}</text>
    <text x="400" y="34" text-anchor="end" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">{games[0]['playtime']}</text>

    <!-- Game 2 -->
    <rect x="0" y="55" width="410" height="30" rx="4" fill="#1C2128"/>
    <rect x="0" y="55" width="4" height="30" rx="2" fill="{games[1]['color']}"/>
    <text x="15" y="74" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="14">{games[1]['name']}</text>
    <text x="400" y="74" text-anchor="end" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">{games[1]['playtime']}</text>

    <!-- Game 3 -->
    <rect x="0" y="95" width="410" height="30" rx="4" fill="#1C2128"/>
    <rect x="0" y="95" width="4" height="30" rx="2" fill="{games[2]['color']}"/>
    <text x="15" y="114" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="14">{games[2]['name']}</text>
    <text x="400" y="114" text-anchor="end" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">{games[2]['playtime']}</text>
  </g>
</svg>"""

    os.makedirs("metrics", exist_ok=True)
    with open("metrics/steam-card.svg", "w") as f:
        f.write(svg_content)
    print("Steam pulse card generated.")

if __name__ == "__main__":
    update_steam()
