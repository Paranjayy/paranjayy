import requests
import re
import os

def update_monkeytype():
    print(f"Syncing Monkeytype Stats...")
    stats = {
        "wpm_15": "90", "wpm_30": "92", "wpm_60": "85",
        "tests": "771", "time": "0h 3m", "xp": "771", "streak": "1"
    }

    # Embedded Logo (User Provided)
    logo_svg = """<g transform="scale(0.18) translate(0, 0)">
        <path d="M250,120C255.519,120 260,124.481 260,130C260,135.519 255.519,140 250,140C244.481,140 240,135.519 240,130C240,124.481 244.481,120 250,120Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M110,120L170,120C175.519,120 180,124.481 180,130C180,135.519 175.519,140 170,140L110,140C104.481,140 100,130C100,124.481 104.481,120 110,120Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M90,60C95.519,60 100,64.481 100,70L100,90C100,95.519 95.519,100 90,100C84.481,100 80,95.519 80,90L80,70C80,64.481 84.481,60 90,60Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M40,120C45.519,120 50,124.481 50,130L50,150C50,155.519 45.519,160 40,160C34.481,160 30,155.519 30,150L30,130C30,124.481 34.481,120 40,120Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M210,120C215.519,120 220,124.481 220,130L220,150C220,155.519 215.519,160 210,160C204.481,160 200,155.519 200,150L200,130C200,124.481 204.481,120 210,120Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M110,40L130,40C135.519,40 140,44.481 140,50C140,55.519 135.519,60 130,60L110,60C104.481,60 100,55.519 100,50C100,44.481 104.481,40 110,40Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M150,80L190,80C195.519,80 200,84.481 200,90C200,95.519 195.519,100 190,100L150,100C144.481,100 140,95.519 140,90C140,84.481 144.481,80 150,80Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
    </g>"""

    svg_content = f"""<svg width="400" height="150" viewBox="0 0 400 150" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="150" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="399" height="149" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  
  <g transform="translate(20, 20)">
    {logo_svg}
    <text x="60" y="24" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">Monkeytype Stats</text>
  </g>

  <g transform="translate(20, 70)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">15 SEC PB</text>
    <text x="0" y="20" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{stats['wpm_15']} <tspan fill="#8B949E" font-weight="normal" font-size="10">WPM</tspan></text>
    <text x="120" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">30 SEC PB</text>
    <text x="120" y="20" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{stats['wpm_30']} <tspan fill="#8B949E" font-weight="normal" font-size="10">WPM</tspan></text>
    <text x="240" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">60 SEC PB</text>
    <text x="240" y="20" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="16">{stats['wpm_60']} <tspan fill="#8B949E" font-weight="normal" font-size="10">WPM</tspan></text>
  </g>

  <line x1="20" y1="110" x2="380" y2="110" stroke="#2D333B" stroke-width="1"/>
  <g transform="translate(20, 132)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">XP: <tspan fill="#F0F6FC" font-weight="bold">{stats['xp']}</tspan></text>
    <text x="80" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">TESTS: <tspan fill="#F0F6FC" font-weight="bold">{stats['tests']}</tspan></text>
    <text x="180" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">STREAK: <tspan fill="#E2B714" font-weight="bold">{stats['streak']} DAYS</tspan></text>
  </g>
</svg>"""

    os.makedirs("metrics", exist_ok=True)
    with open("metrics/monkeytype-card.svg", "w") as f:
        f.write(svg_content)
    print("Monkeytype card updated.")

if __name__ == "__main__":
    update_monkeytype()
