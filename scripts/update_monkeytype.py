import requests
import re
import os

def update_monkeytype():
    print(f"Syncing Monkeytype Stats...")
    # Comprehensive stats from user profile screenshot & snapshots
    stats = {
        "wpm_15": "-", "wpm_30": "92", "wpm_60": "-", "wpm_120": "-",
        "acc_30": "99%",
        "tests_started": "6", "tests_completed": "6", 
        "time_typing": "0h 3m", "xp": "771", "level": "5", 
        "streak": "1", "joined": "02 Feb 2025",
        "words_typed": "142", "chars_typed": "710" # Estimated from time/wpm
    }

    # Official-style Monkeytype Logo (High Fidelity)
    logo_svg = """<g transform="translate(0, 2)">
      <rect width="32" height="32" rx="6" fill="#E2B714"/>
      <path d="M8 22V10H11L16 16L21 10H24V22H21V14L16 20L11 14V22H8Z" fill="#171A20"/>
    </g>"""

    svg_content = f"""<svg width="450" height="230" viewBox="0 0 450 230" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="450" height="230" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="449" height="229" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  
  <!-- Header -->
  <g transform="translate(20, 20)">
    {logo_svg}
    <text x="42" y="24" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">Monkeytype Stats</text>
    <text x="42" y="42" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">Joined {stats['joined']}</text>
  </g>

  <!-- Level & XP -->
  <g transform="translate(320, 25)">
    <text x="100" y="0" text-anchor="end" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">LEVEL</text>
    <text x="100" y="22" text-anchor="end" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="24">{stats['level']}</text>
    <rect x="0" y="30" width="100" height="6" rx="3" fill="#2D333B"/>
    <rect x="0" y="30" width="45" height="6" rx="3" fill="#E2B714"/>
    <text x="100" y="48" text-anchor="end" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="9">77 / 296 XP</text>
  </g>

  <!-- PB Grid -->
  <g transform="translate(20, 90)">
    <rect width="410" height="70" rx="8" fill="#1C2128" fill-opacity="0.5"/>
    
    <g transform="translate(15, 15)">
      <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">15 SEC PB</text>
      <text x="0" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">{stats['wpm_15']}</text>
      
      <text x="100" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">30 SEC PB</text>
      <text x="100" y="25" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="20">{stats['wpm_30']} <tspan font-size="10" font-weight="normal" fill="#8B949E">WPM</tspan></text>
      <text x="100" y="42" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">ACCURACY: <tspan fill="#F0F6FC">{stats['acc_30']}</tspan></text>
      
      <text x="200" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">60 SEC PB</text>
      <text x="200" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">{stats['wpm_60']}</text>

      <text x="300" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">WORDS TYPED</text>
      <text x="300" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">{stats['words_typed']}</text>
      <text x="300" y="42" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">CHARS: <tspan fill="#F0F6FC">{stats['chars_typed']}</tspan></text>
    </g>
  </g>

  <!-- Footer Metrics -->
  <g transform="translate(20, 195)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TESTS: <tspan fill="#F0F6FC" font-weight="bold">{stats['tests_completed']}/{stats['tests_started']}</tspan></text>
    <text x="120" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TIME TYPING: <tspan fill="#F0F6FC" font-weight="bold">{stats['time_typing']}</tspan></text>
    <text x="260" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TOTAL XP: <tspan fill="#F0F6FC" font-weight="bold">{stats['xp']}</tspan></text>
    <text x="360" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">STREAK: <tspan fill="#E2B714" font-weight="bold">{stats['streak']} DAYS</tspan></text>
  </g>
</svg>"""

    os.makedirs("metrics", exist_ok=True)
    with open("metrics/monkeytype-card.svg", "w") as f:
        f.write(svg_content)
    print("Monkeytype comprehensive card updated (Logo fixed & Stats added).")

if __name__ == "__main__":
    update_monkeytype()
