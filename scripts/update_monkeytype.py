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
        "words_typed": "142", "chars_typed": "710",
        "consistency": "94%", "cpm": "460"
    }

    # Official Monkeytype Logo (Traced from provided image)
    logo_svg = """<g transform="scale(0.8) translate(0, 0)">
      <rect x="2" y="5" width="56" height="32" rx="10" stroke="#E2B714" stroke-width="4" fill="none"/>
      <path d="M12 26V18C12 16.5 13 15.5 14.5 15.5C16 15.5 17 16.5 17 18V26M17 18C17 16.5 18 15.5 19.5 15.5C21 15.5 22 16.5 22 18V26" stroke="#E2B714" stroke-width="3" stroke-linecap="round" fill="none"/>
      <circle cx="34" cy="15" r="2.5" fill="#E2B714"/>
      <rect x="39" y="13.5" width="10" height="3" rx="1.5" fill="#E2B714"/>
      <rect x="32" y="22" width="20" height="3" rx="1.5" fill="#E2B714"/>
      <rect x="32" y="28" width="8" height="3" rx="1.5" fill="#E2B714"/>
      <circle cx="48" cy="29.5" r="2.5" fill="#E2B714"/>
    </g>"""

    svg_content = f"""<svg width="450" height="240" viewBox="0 0 450 240" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="450" height="240" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="449" height="239" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  
  <!-- Header -->
  <g transform="translate(20, 20)">
    {logo_svg}
    <text x="55" y="24" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="20">Monkeytype Stats</text>
    <text x="55" y="44" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">Joined {stats['joined']}</text>
  </g>

  <!-- Level & XP -->
  <g transform="translate(320, 25)">
    <text x="100" y="0" text-anchor="end" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">LEVEL</text>
    <text x="100" y="22" text-anchor="end" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="24">{stats['level']}</text>
    <rect x="0" y="30" width="100" height="6" rx="3" fill="#2D333B"/>
    <rect x="0" y="30" width="45" height="6" rx="3" fill="#E2B714"/>
    <text x="100" y="48" text-anchor="end" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="9">77 / 296 XP</text>
  </g>

  <!-- PB & Performance Grid -->
  <g transform="translate(20, 95)">
    <rect width="410" height="85" rx="8" fill="#1C2128" fill-opacity="0.5"/>
    
    <g transform="translate(15, 15)">
      <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">15 SEC PB</text>
      <text x="0" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">{stats['wpm_15']}</text>
      
      <text x="100" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">30 SEC PB</text>
      <text x="100" y="25" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="22">{stats['wpm_30']} <tspan font-size="10" font-weight="normal" fill="#8B949E">WPM</tspan></text>
      <text x="100" y="45" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">ACCURACY: <tspan fill="#F0F6FC">{stats['acc_30']}</tspan></text>
      <text x="100" y="60" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">CONSISTENCY: <tspan fill="#F0F6FC">{stats['consistency']}</tspan></text>
      
      <text x="210" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">60 SEC PB</text>
      <text x="210" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">{stats['wpm_60']}</text>

      <text x="310" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">WORDS TYPED</text>
      <text x="310" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">{stats['words_typed']}</text>
      <text x="310" y="45" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">CPM: <tspan fill="#F0F6FC">{stats['cpm']}</tspan></text>
      <text x="310" y="60" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="10">CHARS: <tspan fill="#F0F6FC">{stats['chars_typed']}</tspan></text>
    </g>
  </g>

  <!-- Footer Metrics -->
  <g transform="translate(20, 210)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TESTS COMPLETED: <tspan fill="#F0F6FC" font-weight="bold">{stats['tests_completed']}</tspan></text>
    <text x="140" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TIME TYPING: <tspan fill="#F0F6FC" font-weight="bold">{stats['time_typing']}</tspan></text>
    <text x="270" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TOTAL XP: <tspan fill="#F0F6FC" font-weight="bold">{stats['xp']}</tspan></text>
    <text x="360" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">STREAK: <tspan fill="#E2B714" font-weight="bold">{stats['streak']} DAYS</tspan></text>
  </g>
</svg>"""

    os.makedirs("metrics", exist_ok=True)
    with open("metrics/monkeytype-card.svg", "w") as f:
        f.write(svg_content)
    print("Monkeytype comprehensive card updated (Logo fixed & Stats expanded).")

if __name__ == "__main__":
    update_monkeytype()
