import requests
import os

def update_leetcode():
    print(f"Syncing LeetCode Intelligence...")
    # Prototype with baseline data
    # In a real scenario, we'd use a GraphQL query to LeetCode
    data = {
        "solved": "214", "total": "3200", "rank": "184,203", 
        "easy": "120", "medium": "84", "hard": "10",
        "streak": "12"
    }

    svg_content = f"""<svg width="450" height="150" viewBox="0 0 450 150" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="450" height="150" rx="12" fill="#171A20"/>
  <rect x="0.5" y="0.5" width="449" height="149" rx="11.5" stroke="#2D333B" stroke-opacity="0.5"/>
  
  <g transform="translate(20, 20)">
    <path d="M16 2L2 16L16 30L30 16L16 2ZM16 7L25 16L16 25L7 16L16 7Z" fill="#FFA116"/>
    <text x="40" y="24" fill="#FFA116" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="18">LeetCode Pulse</text>
  </g>

  <g transform="translate(20, 75)">
    <text x="0" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">SOLVED</text>
    <text x="0" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="24">{data['solved']} <tspan fill="#8B949E" font-size="12" font-weight="normal">/ {data['total']}</tspan></text>
    
    <text x="160" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">GLOBAL RANK</text>
    <text x="160" y="25" fill="#F0F6FC" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="20">#{data['rank']}</text>

    <text x="320" y="0" fill="#8B949E" font-family="Segoe UI, sans-serif" font-size="11">STREAK</text>
    <text x="320" y="25" fill="#FFA116" font-family="Segoe UI, sans-serif" font-weight="bold" font-size="20">{data['streak']} DAYS</text>
  </g>

  <g transform="translate(20, 130)">
    <rect width="410" height="4" rx="2" fill="#2D333B"/>
    <rect width="180" height="4" rx="2" fill="#00B8A3"/> <!-- Easy -->
    <rect x="180" width="120" height="4" rx="2" fill="#FFC01E"/> <!-- Medium -->
    <rect x="300" width="20" height="4" rx="2" fill="#FF375F"/> <!-- Hard -->
  </g>
</svg>"""

    os.makedirs("metrics", exist_ok=True)
    with open("metrics/leetcode-card.svg", "w") as f:
        f.write(svg_content)
    print("LeetCode pulse card generated.")

if __name__ == "__main__":
    update_leetcode()
