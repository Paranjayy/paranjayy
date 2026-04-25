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
        
        completed_tests = data["typingStats"]["completedTests"]
        time_typing_seconds = data["typingStats"]["timeTyping"]
        
        # Format Time (MM:SS)
        minutes = time_typing_seconds // 60
        seconds = time_typing_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        # 2. Update SVG Template
        svg_path = "metrics/monkeytype-card.svg"
        if not os.path.exists(svg_path):
            print(f"Error: {svg_path} not found.")
            return
            
        with open(svg_path, "r") as f:
            content = f.read()
            
        # Regex replacements for the specific SVG structure I built
        content = re.sub(r'(fill="#e2b714">)\d+(</text>)', rf'\g<1>{wpm}\g<2>', content) # WPM
        content = re.sub(r'(fill="#d1d0c5">)\d+%(</text>)', rf'\g<1>{acc}%\g<2>', content) # Accuracy
        content = re.sub(r'(tests completed:.*fill="#d1d0c5">)\d+(</text>)', rf'\g<1>{completed_tests}\g<2>', content) # Tests
        content = re.sub(r'(typing time:.*fill="#d1d0c5">)\d+:\d+(</text>)', rf'\g<1>{time_str}\g<2>', content) # Time
        
        # Update Progress Bar (Subtle logic: map completed tests to width 0-360, capping at 360 for now)
        progress_width = min(360, (completed_tests / 10) * 360) # Visual progress toward 10 tests
        content = re.sub(r'(width=")\d+(" height="4" rx="2" fill="#e2b714")', rf'\g<1>{int(progress_width)}\g<2>', content)

        with open(svg_path, "w") as f:
            f.write(content)
            
        print(f"Successfully updated Monkeytype stats: {wpm} WPM, {acc}% Accuracy")
        
    except Exception as e:
        print(f"Failed to update Monkeytype: {e}")

if __name__ == "__main__":
    update_monkeytype()
