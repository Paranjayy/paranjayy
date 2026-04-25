import requests
import re
import os

def update_monkeytype():
    print(f"Syncing Monkeytype Stats...")
    # Comprehensive stats from user profile screenshot & snapshots
    stats = {
        "wpm_15": "-", "wpm_30": "92", "wpm_60": "-", "wpm_120": "-",
        "tests_started": "6", "tests_completed": "6", 
        "time_typing": "0h 3m", "xp": "771", "level": "5", 
        "streak": "1", "joined": "02 Feb 2025"
    }

    # Better Monkeytype Logo (Simplified & Premium)
    # Using a professional geometric representation
    logo_svg = """<g transform="scale(0.8) translate(5, 5)">
        <path d="M20 5C11.7157 5 5 11.7157 5 20C5 28.2843 11.7157 35 20 35C28.2843 35 35 28.2843 35 20C35 11.7157 28.2843 5 20 5ZM2 20C2 10.0589 10.0589 2 20 2C29.9411 2 38 10.0589 38 20C38 29.9411 29.9411 38 20 38C10.0589 38 2 29.9411 2 20Z" fill="#E2B714"/>
        <path d="M15 18C16.6569 18 18 16.6569 18 15C18 13.3431 16.6569 12 15 12C13.3431 12 12 13.3431 12 15C12 16.6569 13.3431 18 15 18Z" fill="#E2B714"/>
        <path d="M25 18C26.6569 18 28 16.6569 28 15C28 13.3431 26.6569 12 25 12C23.3431 12 22 13.3431 22 15C22 16.6569 23.3431 18 25 18Z" fill="#E2B714"/>
        <path d="M20 28C24 28 27 25 27 25" stroke="#E2B714" stroke-width="2" stroke-linecap="round"/>
    </g>"""

    svg_content = f"""<svg width="450" height="230" viewBox="0 0 450 230" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="450" height="230" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="449" height="229" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  
  <!-- Header -->
  <g transform="translate(20, 20)">
    {logo_svg}
    <text x="45" y="24" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">Monkeytype Stats</text>
    <text x="45" y="42" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">Joined {stats['joined']}</text>
  </g>

  <!-- Level & XP -->
  <g transform="translate(320, 25)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">LEVEL</text>
    <text x="0" y="22" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="24">{stats['level']}</text>
    <rect x="0" y="30" width="100" height="6" rx="3" fill="#2D333B"/>
    <rect x="0" y="30" width="45" height="6" rx="3" fill="#E2B714"/>
    <text x="0" y="48" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="9">77 / 296 XP</text>
  </g>

  <!-- PB Grid -->
  <g transform="translate(20, 90)">
    <rect width="410" height="60" rx="8" fill="#1C2128" fill-opacity="0.5"/>
    
    <g transform="translate(15, 15)">
      <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">15 SEC PB</text>
      <text x="0" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">{stats['wpm_15']}</text>
      
      <text x="100" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">30 SEC PB</text>
      <text x="100" y="25" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="20">{stats['wpm_30']} <tspan font-size="10" font-weight="normal" fill="#8B949E">WPM</tspan></text>
      
      <text x="200" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">60 SEC PB</text>
      <text x="200" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">{stats['wpm_60']}</text>

      <text x="300" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">120 SEC PB</text>
      <text x="300" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">{stats['wpm_120']}</text>
    </g>
  </g>

  <!-- Detailed Metrics -->
  <g transform="translate(20, 180)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TESTS: <tspan fill="#F0F6FC" font-weight="bold">{stats['tests_completed']}/{stats['tests_started']}</tspan></text>
    <text x="120" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TIME TYPING: <tspan fill="#F0F6FC" font-weight="bold">{stats['time_typing']}</tspan></text>
    <text x="260" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TOTAL XP: <tspan fill="#F0F6FC" font-weight="bold">{stats['xp']}</tspan></text>
    <text x="360" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">STREAK: <tspan fill="#E2B714" font-weight="bold">{stats['streak']} DAYS</tspan></text>
  </g>
</svg>"""

    os.makedirs("metrics", exist_ok=True)
    with open("metrics/monkeytype-card.svg", "w") as f:
        f.write(svg_content)
    print("Monkeytype comprehensive card updated.")

if __name__ == "__main__":
    update_monkeytype()
