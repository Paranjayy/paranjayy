import requests
import re
import os

# --- HOW TO PERSONALIZE ---
# 1. Change the username in the requests.get() URL below.
# 2. Ensure your Monkeytype profile is public.
# 3. This script will automatically update metrics/monkeytype-card.svg.
# --------------------------

def update_monkeytype():
    try:
        # 1. Fetch Latest Stats
        username = "paranjayy"
        response = requests.get(f"https://api.monkeytype.com/users/{username}/profile")
        response.raise_for_status()
        data = response.json()["data"]
        
        pbs = data.get("personalBests", {})
        time_pbs = pbs.get("time", {})
        word_pbs = pbs.get("words", {})
        
        all_time_lbs = data.get("allTimeLbs", {}).get("time", {})
        
        typing_stats = data.get("typingStats", {})
        completed_tests = typing_stats.get("completedTests", 0)
        time_typing_seconds = typing_stats.get("timeTyping", 0)
        xp = data.get("xp", 0)
        streak = data.get("streak", 0)
        
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
            
        def get_pb_vals(category, key):
            mode_data = category.get(str(key))
            if mode_data:
                pb = mode_data[0]
                return round(pb["wpm"]), round(pb["acc"])
            return "-", "-"

        def get_rank_str(time_key):
            lb_data = all_time_lbs.get(str(time_key))
            if lb_data and lb_data.get("rank"):
                rank = lb_data["rank"]
                # Add suffix
                if 11 <= (rank % 100) <= 13:
                    suffix = "th"
                else:
                    suffix = {1: "st", 2: "nd", 3: "rd"}.get(rank % 10, "th")
                return f"{rank}{suffix}"
            return "-"

        # Update Time-based PBs & Ranks
        for t in [15, 30, 60, 120]:
            wpm, acc = get_pb_vals(time_pbs, t)
            rank = get_rank_str(t)
            acc_val = f"{acc}%" if acc != "-" else "-"
            
            # Find the specific block for the time value
            pattern = rf'(<text x="0" y="0" class="stat-label">{t} seconds</text>\s+<text x="0" y="22" class="stat-wpm">).*?(</text>\s+<text x="0" y="38" class="stat-acc">).*?(</text>\s+<text x="0" y="52" class="stat-rank">).*?(</text>)'
            content = re.sub(pattern, rf'\g<1>{wpm}\g<2>{acc_val}\g<3>{rank}\g<4>', content, flags=re.DOTALL)

        # Update Word-based PBs
        for w in [10, 25, 50, 100]:
            wpm, acc = get_pb_vals(word_pbs, w)
            acc_val = f"{acc}%" if acc != "-" else "-"
            pattern = rf'(<text x="0" y="0" class="stat-label">{w} words</text>\s+<text x="0" y="22" class="stat-wpm">).*?(</text>\s+<text x="0" y="38" class="stat-acc">).*?(</text>)'
            content = re.sub(pattern, rf'\g<1>{wpm}\g<2>{acc_val}\g<3>', content, flags=re.DOTALL)

        # Update Footer Stats
        content = re.sub(r'(tests completed:.*class="meta-value">)\d+(</text>)', rf'\g<1>{completed_tests}\g<2>', content)
        content = re.sub(r'(typing time:.*class="meta-value">)\d+:\d+(</text>)', rf'\g<1>{time_str}\g<2>', content)
        content = re.sub(r'(xp earned:.*class="meta-value">)\d+(</text>)', rf'\g<1>{xp}\g<2>', content)
        content = re.sub(r'(streak:.*class="meta-value">)\d+(</text>)', rf'\g<1>{streak}\g<2>', content)
        
        # Accent bar progress
        main_wpm, _ = get_pb_vals(time_pbs, 30)
        if main_wpm != "-":
            progress_width = (float(main_wpm) / 100) * 550
            content = re.sub(r'(width=")\d+(\.?\d*)(" height="3" rx="1.5" fill="#e2b714")', rf'\g<1>{progress_width}\g<2>', content)

        with open(svg_path, "w") as f:
            f.write(content)
            
        print("Successfully updated Hyper-Granular Monkeytype stats with Ranks.")
        
    except Exception as e:
        print(f"Failed to update Monkeytype: {e}")

if __name__ == "__main__":
    update_monkeytype()
