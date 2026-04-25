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

    # User provided Monkeytype Logo
    logo_svg = """<g transform="scale(0.15) translate(0, 0)">
        <path d="M250,120C255.519,120 260,124.481 260,130C260,135.519 255.519,140 250,140C244.481,140 240,135.519 240,130C240,124.481 244.481,120 250,120Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M110,120L170,120C175.519,120 180,124.481 180,130C180,135.519 175.519,140 170,140L110,140C104.481,140 100,135.519 100,130C100,124.481 104.481,120 110,120Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M90,60C95.519,60 100,64.481 100,70L100,90C100,95.519 95.519,100 90,100C84.481,100 80,95.519 80,90L80,70C80,64.481 84.481,60 90,60Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M40.009,69.485C40.28,53.164 53.615,40 70,40C77.68,40 84.69,42.892 90,47.645C95.31,42.892 102.32,40 110,40C126.385,40 139.72,53.164 139.991,69.485C139.999,69.655 140,69.828 140,70L140,90C140,95.519 135.519,100 130,100C124.481,100 120,95.519 120,90L120,70C120,64.481 115.519,60 110,60C104.481,60 100,64.481 100,70L100,90C100,95.519 95.519,100 90,100C84.481,100 80,95.519 80,90L80,70C80,64.481 75.519,60 70,60C64.481,60 60,64.481 60,70L60,90C60,95.519 55.519,100 50,100C44.481,100 40,95.519 40,90L40,70C40,69.828 40.004,69.656 40.009,69.485Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M220,100L220,130C220,135.519 215.519,140 210,140C204.481,140 200,135.519 200,130L200,100L171.18,100C165.01,100 160,95.519 160,90C160,84.481 165.01,80 171.18,80L248.82,80C254.99,80 260,84.481 260,90C260,95.519 254.99,100 248.82,100L220,100Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M210,40L250,40C255.519,40 260,44.481 260,50C260,55.519 255.519,60 250,60L210,60C204.481,60 200,55.519 200,50C200,44.481 204.481,40 210,40Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M50,120L70,120C75.519,120 80,124.481 80,130C80,135.519 75.519,140 70,140L50,140C44.481,140 40,135.519 40,130C40,124.481 44.481,120 50,120Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M165,40L170,40C175.519,40 180,44.481 180,50C180,55.519 175.519,60 170,60L165,60C159.481,60 155,55.519 155,50C155,44.481 159.481,40 165,40Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
        <path d="M20,110L0,110L0,50C0,22.404 22.404,0 50,0L250,0C277.596,0 300,22.404 300,50L300,130C300,157.596 277.596,180 250,180L50,180C22.404,180 0,157.596 0,130L0,110L20,110L20,130C20,146.557 33.443,160 50,160L250,160C266.557,160 280,146.557 280,130L280,50C280,33.443 266.557,20 250,20L50,20C33.443,20 20,33.443 20,50L20,110Z" style="fill:rgb(226,183,20);fill-rule:nonzero;"/>
    </g>"""

    svg_content = f"""<svg width="450" height="260" viewBox="0 0 450 260" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="450" height="260" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="449" height="259" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  
  <!-- Header -->
  <g transform="translate(20, 20)">
    {logo_svg}
    <text x="55" y="16" fill="#E2B714" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="20">Monkeytype Stats</text>
    <text x="55" y="34" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="12">Joined {stats['joined']}</text>
  </g>

  <!-- Level & XP -->
  <g transform="translate(320, 20)">
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
    print("Monkeytype comprehensive card updated (Original Logo & Fixed Cropping).")

if __name__ == "__main__":
    update_monkeytype()
