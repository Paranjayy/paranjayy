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

  <text x="25" y="35" class="header">Monkeytype Intelligence</text>
  
  <!-- Personal Bests -->
  <g transform="translate(25, 70)">
    <text x="0" y="0" class="stat-label">15 SEC PB</text>
    <text x="0" y="25" class="stat-value">{wpm_15} <tspan font-size="12" font-weight="normal" fill="#646669">WPM</tspan></text>
    
    <text x="160" y="0" class="stat-label">30 SEC PB</text>
    <text x="160" y="25" class="stat-value">{wpm_30} <tspan font-size="12" font-weight="normal" fill="#646669">WPM</tspan></text>
    
    <text x="320" y="0" class="stat-label">60 SEC PB</text>
    <text x="320" y="25" class="stat-value">{wpm_60} <tspan font-size="12" font-weight="normal" fill="#646669">WPM</tspan></text>
  </g>

  <!-- Divider -->
  <line x1="25" y1="130" x2="475" y2="130" stroke="#2D333B" stroke-width="1"/>

  <!-- Footer Stats -->
  <g transform="translate(25, 160)">
    <text x="0" y="0" class="meta-label">TESTS COMPLETED: <tspan class="meta-value">{tests_completed}</tspan></text>
    <text x="140" y="0" class="meta-label">TIME TYPING: <tspan class="meta-value">{hours}h {minutes}m</tspan></text>
    <text x="260" y="0" class="meta-label">XP: <tspan class="meta-value">{xp:,}</tspan></text>
    <text x="380" y="0" class="meta-label">STREAK: <tspan class="meta-value">{streak} DAYS</tspan></text>
  </g>
</svg>"""

        os.makedirs("metrics", exist_ok=True)
        with open("metrics/monkeytype-card.svg", "w") as f:
            f.write(svg_content)
        print("Monkeytype card regenerated successfully.")

    except Exception as e:
        print(f"Error updating Monkeytype: {e}")

if __name__ == "__main__":
    update_monkeytype()
