import re
import os

def update_typing_svg():
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the WakaTime code time from the shields badge
    # Example: ![Code Time](http://img.shields.io/badge/Code%20Time-54%20hrs%2020%20mins-blue?style=flat)
    match = re.search(r"Code%20Time-([\d% a-zA-Z]+)-blue", content)
    if not match:
        print("WakaTime code time badge not found")
        return

    raw_time = match.group(1)
    # Clean up the time string (replace %20 with space)
    clean_time = raw_time.replace("%20", " ")
    
    # We want something like "~54 hrs coded this month"
    # The badge might say "54 hrs 20 mins"
    # We'll just take the hours part or the whole thing
    display_time = f"~{clean_time} coded this month"
    
    # URL encode the spaces for the SVG URL
    encoded_time = display_time.replace(" ", "+").replace("&", "%26")

    # Find the typing SVG URL
    # Example: img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=25&pause=1000&color=19FFD6&center=true&vCenter=true&width=800&lines=An+Aspiring+SDE;Currently+Learning+%26+Exploring+%F0%9F%93%9A;~54+hrs+coded+this+month+%E2%8C%A8%EF%B8%8F"
    # We need to replace the last part of 'lines='
    
    pattern = r'(https://readme-typing-svg\.herokuapp\.com\?[^"]+lines=[^;"]+;[^;"]+;)([^"]+)'
    new_content = re.sub(pattern, r'\1' + encoded_time + r'%20%E2%8C%A8%EF%B8%8F', content)

    if new_content != content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated typing SVG with: {display_time}")
    else:
        print("No changes made to typing SVG")

if __name__ == "__main__":
    update_typing_svg()
