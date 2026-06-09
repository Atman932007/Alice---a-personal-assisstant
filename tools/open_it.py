import subprocess
import re

# These are all the sites 

Known_sites = {
    "youtube"       : "https://youtube.com",
    "google"        : "https://google.com",
    "gmail"         : "https://mail.google.com",
    "google maps"   : "https://maps.google.com",
    "maps"          : "https://maps.google.com",
    "instagram"     : "https://instagram.com",
    "twitter"       : "https://twitter.com",
    "x"             : "https://twitter.com",
    "facebook"      : "https://facebook.com",
    "github"        : "https://github.com",
    "netflix"       : "https://netflix.com",
    "amazon"        : "https://amazon.in",
    "flipkart"      : "https://flipkart.com",
    "wikipedia"     : "https://wikipedia.org",
    "reddit"        : "https://reddit.com",
    "stackoverflow" : "https://stackoverflow.com",
    "chatgpt"       : "https://chat.openai.com",
    "linkedin"      : "https://linkedin.com",
}

# These are all the apps present on my macbook

Mac_apps = {
    "whatsapp"  : "WhatsApp",
    "spotify"   : "Spotify",
    "discord"   : "Discord",
    "telegram"  : "Telegram",
    "slack"     : "Slack",
    "zoom"      : "Zoom",
    "facetime"  : "FaceTime",
    "notes"     : "Notes",
    "calendar"  : "Calendar",
    "maps"      : "Maps",
    "music"     : "Music",
    "photos"    : "Photos",
    "settings"  : "System Settings",
    "vs code"   : "Visual Studio Code"
}

# Creating a function to open sites

def open_it(question: str) -> str:
    question_lower = question.lower()

    # Opening apps

    for app_name, app_command in Mac_apps.items():
        if app_name in question_lower:
            try:
                subprocess.run(["open", "-a", app_command])
                return f"Opening {app_command} sir"
            except:
                return f"I was unable to find {app_command}"

    # Opening sites

    for site_name, url in Known_sites.items():
        if site_name in question_lower:
            subprocess.run(["open", url])
            return f"Opening {site_name} sir."

    # Matching the url for searching on web

    url_pattern = r'https?://[^\s]+'
    url_match = re.search(url_pattern, question_lower)
    if url_match:
        url = url_match.group()
        subprocess.run(["open", url])
        return f"Opening the website sir."
    
    # Searching for unknown sites

    words = question_lower.replace("open", " ").replace("launch", " ").replace("go to", " ").replace("website", " ").strip()
    if words:
        search_url = f"https://google.com/search?q={words.replace(' ', '+')}"
        subprocess.run(["open", search_url])
        return f"I searched Google for {words} sir."
    return "I am not sure what to open sir, could you be more specific?"

# Testing block

if __name__ == "__main__":
    result = open_it("open youtube")
    print(result)
    