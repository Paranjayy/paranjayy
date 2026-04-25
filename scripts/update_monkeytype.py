import requests
import os

def update_monkeytype():
    username = "paranjayy"
    print(f"Fetching Monkeytype stats for {username}...")
    
    try:
        response = requests.get(f"https://api.monkeytype.com/users/{username}/profile")
        response.raise_for_status()
        data = response.json()["data"]
        
        # Extract core stats
        pbs = data.get("personalBests", {}).get("time", {})
        wpm_15 = round(pbs.get("15", [{}])[0].get("wpm", 0)) if pbs.get("15") else "-"
        wpm_30 = round(pbs.get("30", [{}])[0].get("wpm", 0)) if pbs.get("30") else "-"
        wpm_60 = round(pbs.get("60", [{}])[0].get("wpm", 0)) if pbs.get("60") else "-"
        
        typing_stats = data.get("typingStats", {})
        tests_completed = typing_stats.get("completedTests", 0)
        time_typing_seconds = typing_stats.get("timeTyping", 0)
        hours = time_typing_seconds // 3600
        minutes = (time_typing_seconds % 3600) // 60
        
        xp = data.get("xp", 0)
        streak = data.get("streak", 0)

        # SVG Generation (High Fidelity, Self-Contained)
        svg_content = f"""<svg width="500" height="200" viewBox="0 0 500 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .header {{ font: bold 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #e2b714; }}
    .stat-label {{ font: 600 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #646669; }}
    .stat-value {{ font: bold 24px 'Segoe UI', Ubuntu, Sans-Serif; fill: #e2b714; }}
    .meta-label {{ font: 500 11px 'Segoe UI', Ubuntu, Sans-Serif; fill: #646669; }}
    .meta-value {{ font: bold 11px 'Segoe UI', Ubuntu, Sans-Serif; fill: #d1d0c5; }}
  </style>
  
  <rect width="500" height="200" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="499" height="199" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>

  <!-- Logo Integration -->
  <g transform="translate(25, 20) scale(0.12)">
    <path d="M250,120C255.519,120 260,124.481 260,130C260,135.519 255.519,140 250,140C244.481,140 240,135.519 240,130C240,124.481 244.481,120 250,120Z" fill="#e2b714"/>
    <path d="M110,120L170,120C175.519,120 180,124.481 180,130C180,135.519 175.519,140 170,140L110,140C104.481,140 100,135.519 100,130C100,124.481 104.481,120 110,120Z" fill="#e2b714"/>
    <path d="M90,60C95.519,60 100,64.481 100,70L100,90C100,95.519 95.519,100 90,100C84.481,100 80,95.519 80,90L80,70C80,64.481 84.481,60 90,60Z" fill="#e2b714"/>
    <path d="M40.009,69.485C40.28,53.164 53.615,40 70,40C77.68,40 84.69,42.892 90,47.645C95.31,42.892 102.32,40 110,40C126.385,40 139.72,53.164 139.991,69.485C139.999,69.655 140,69.828 140,70L140,90C140,95.519 135.519,100 130,100C124.481,100 120,95.519 120,90L120,70C120,64.481 115.519,60 110,60C104.481,60 100,64.481 100,70L100,90C100,95.519 95.519,100 90,100C84.481,100 80,95.519 80,90L80,70C80,64.481 75.519,60 70,60C64.481,60 60,64.481 60,70L60,90C60,95.519 55.519,100 50,100C44.481,100 40,95.519 40,90L40,70C40,69.828 40.004,69.656 40.009,69.485Z" fill="#e2b714"/>
    <path d="M220,100L220,130C220,135.519 215.519,140 210,140C204.481,140 200,135.519 200,130L200,100L171.18,100C165.01,100 160,95.519 160,90C160,84.481 165.01,80 171.18,80L248.82,80C254.99,80 260,84.481 260,90C260,95.519 254.99,100 248.82,100L220,100Z" fill="#e2b714"/>
    <path d="M210,40L250,40C255.519,40 260,44.481 260,50C260,55.519 255.519,60 250,60L210,60C204.481,60 200,55.519 200,50C200,44.481 204.481,40 210,40Z" fill="#e2b714"/>
    <path d="M50,120L70,120C75.519,120 80,124.481 80,130C80,135.519 75.519,140 70,140L50,140C44.481,140 40,135.519 40,130C40,124.481 44.481,120 50,120Z" fill="#e2b714"/>
    <path d="M165,40L170,40C175.519,40 180,44.481 180,50C180,55.519 175.519,60 170,60L165,60C159.481,60 155,55.519 155,50C155,44.481 159.481,40 165,40Z" fill="#e2b714"/>
    <path d="M20,110L0,110L0,50C0,22.404 22.404,0 50,0L250,0C277.596,0 300,22.404 300,50L300,130C300,157.596 277.596,180 250,180L50,180C22.404,180 0,157.596 0,130L0,110L20,110L20,130C20,146.557 33.443,160 50,160L250,160C266.557,160 280,146.557 280,130L280,50C280,33.443 266.557,20 250,20L50,20C33.443,20 20,33.443 20,50L20,110Z" fill="#e2b714"/>
  </g>

  <text x="75" y="35" class="header">Monkeytype Stats</text>
  
  <!-- Personal Bests -->
  <g transform="translate(25, 75)">
    <text x="0" y="0" class="stat-label">15 SEC PB</text>
    <text x="0" y="25" class="stat-value">{wpm_15} <tspan font-size="12" font-weight="normal" fill="#646669">WPM</tspan></text>
    
    <text x="160" y="0" class="stat-label">30 SEC PB</text>
    <text x="160" y="25" class="stat-value">{wpm_30} <tspan font-size="12" font-weight="normal" fill="#646669">WPM</tspan></text>
    
    <text x="320" y="0" class="stat-label">60 SEC PB</text>
    <text x="320" y="25" class="stat-value">{wpm_60} <tspan font-size="12" font-weight="normal" fill="#646669">WPM</tspan></text>
  </g>

  <!-- Divider -->
  <line x1="25" y1="135" x2="475" y2="135" stroke="#2D333B" stroke-width="1"/>

  <!-- Footer Stats -->
  <g transform="translate(25, 165)">
    <text x="0" y="0" class="meta-label">TESTS COMPLETED: <tspan class="meta-value">{tests_completed}</tspan></text>
    <text x="140" y="0" class="meta-label">TIME TYPING: <tspan class="meta-value">{hours}h {minutes}m</tspan></text>
    <text x="260" y="0" class="meta-label">XP: <tspan class="meta-value">{xp:,}</tspan></text>
    <text x="380" y="0" class="meta-label">STREAK: <tspan class="meta-value">{streak} DAYS</tspan></text>
  </g>
</svg>"""

        os.makedirs("metrics", exist_ok=True)
        with open("metrics/monkeytype-card.svg", "w") as f:
            f.write(svg_content)
        print("Monkeytype card updated with new logo and 'unslopified' name.")

    except Exception as e:
        print(f"Error updating Monkeytype: {e}")

if __name__ == "__main__":
    update_monkeytype()
