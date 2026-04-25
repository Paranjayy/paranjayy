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
        raw_acc = 0.0
        if "30" in data.get("personalBests", {}).get("time", {}):
            pb = data["personalBests"]["time"]["30"][0]
            wpm = round(pb["wpm"])
            acc = round(pb["acc"])
            raw_acc = pb["acc"]
        
        completed_tests = data["typingStats"]["completedTests"]
        time_typing_seconds = data["typingStats"]["timeTyping"]
        xp = data.get("xp", 0)
        
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
            
        # Regex updates for Feature-Rich Card
        content = re.sub(r'(class="stat-value">)\d+(</text>)', rf'\g<1>{wpm}\g<2>', content) # WPM
        content = re.sub(r'(class="stat-value-sub">)\d+%(</text>)', rf'\g<1>{acc}%\g<2>', content) # Accuracy
        content = re.sub(r'(class="small-label">)\d+\.\d+% raw(</text>)', rf'\g<1>{raw_acc}% raw\g<2>', content) # Raw Acc
        
        content = re.sub(r'(tests completed:.*class="small-value">)\d+(</text>)', rf'\g<1>{completed_tests}\g<2>', content) # Tests
        content = re.sub(r'(typing time:.*class="small-value">)\d+:\d+(</text>)', rf'\g<1>{time_str}\g<2>', content) # Time
        content = re.sub(r'(xp earned:.*class="small-value">)\d+(</text>)', rf'\g<1>{xp}\g<2>', content) # XP
        
        # Precision Bar (based on accuracy)
        progress_width = (acc / 100) * 450
        content = re.sub(r'(width=")\d+(\.?\d*)(" height="4" rx="2" fill="#e2b714")', rf'\g<1>{progress_width}\g<2>', content)

        with open(svg_path, "w") as f:
            f.write(content)
            
        print(f"Successfully updated Monkeytype stats: {wpm} WPM, {acc}% Accuracy, {xp} XP")
        
    except Exception as e:
        print(f"Failed to update Monkeytype: {e}")

if __name__ == "__main__":
    update_monkeytype()
