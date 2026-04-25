import requests
import re
import os

def update_monkeytype():
    try:
        # 1. Fetch Latest Stats
        response = requests.get("https://api.monkeytype.com/users/paranjayy/profile")
        response.raise_for_status()
        data = response.json()["data"]
        
        # Extract Core Stats
        wpm = 0
        acc = 0
        if "30" in data.get("personalBests", {}).get("time", {}):
            pb = data["personalBests"]["time"]["30"][0]
            wpm = round(pb["wpm"])
            acc = round(pb["acc"])
        
        # 2. Update SVG Template
        svg_path = "metrics/monkeytype-card.svg"
        if not os.path.exists(svg_path):
            print(f"Error: {svg_path} not found.")
            return
            
        with open(svg_path, "r") as f:
            content = f.read()
            
        # Updated Regex for the Minimal Card
        content = re.sub(r'(fill="#e2b714">)\d+(</text>)', rf'\g<1>{wpm}\g<2>', content) # WPM
        content = re.sub(r'(fill="#d1d0c5">)\d+%(</text>)', rf'\g<1>{acc}%\g<2>', content) # Accuracy
        
        # Accent bar progress (based on XP/Streak/etc, or just a fixed aesthetic width)
        # Let's use accuracy to fill the bar as a "precision" indicator
        progress_width = (acc / 100) * 350
        content = re.sub(r'(width=")\d+(\.?\d*)(" height="2" rx="1" fill="#e2b714")', rf'\g<1>{progress_width}\g<2>', content)

        with open(svg_path, "w") as f:
            f.write(content)
            
        print(f"Successfully updated Monkeytype stats: {wpm} WPM, {acc}% Accuracy")
        
    except Exception as e:
        print(f"Failed to update Monkeytype: {e}")

if __name__ == "__main__":
    update_monkeytype()
