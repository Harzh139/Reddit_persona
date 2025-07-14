import praw
import re
from datetime import datetime

# Replace with your actual credentials
reddit = praw.Reddit(
    client_id="avP-wmjTHvNKwrSx9YTHgQ",
    client_secret=None,
    refresh_token="105745183306795-z8dT7v_Z-Pk8Kq8xy9BHUJDfrSSJeg",
    user_agent="windows:reddit_persona:v1.0 (by u/YOUR_USERNAME)"
)

def scrape_user_data(username, limit=100):
    user = reddit.redditor(username)
    posts, comments = [], []

    for submission in user.submissions.new(limit=limit):
        posts.append({
            "type": "post",
            "title": submission.title,
            "body": submission.selftext,
            "url": f"https://www.reddit.com{submission.permalink}"
        })

    for comment in user.comments.new(limit=limit):
        comments.append({
            "type": "comment",
            "body": comment.body,
            "url": f"https://www.reddit.com{comment.permalink}"
        })

    return posts + comments

def extract_field(data, keyword_patterns, label):
    for item in data:
        text = item.get("body", "") + " " + item.get("title", "")
        for pattern in keyword_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(), item["url"]
    return "Unknown", None

def build_persona(data, username):
    persona = {
        "Name": username.capitalize(),
        "Age": "Unknown",
        "Occupation": "Unknown",
        "Status": "Unknown",
        "Location": "Unknown",
        "Tier": "Early Adopters",
        "Archetype": "The Explorer",
        "Quote": "",
        "Motivations": [],
        "Personality": [],
        "Behaviours": [],
        "Frustrations": [],
        "Goals": [],
        "Citations": {}
    }

    for item in data:
        text = (item.get("body") or "") + " " + item.get("title", "")
        url = item["url"]

        # Quote
        if not persona["Quote"] and re.search(r"\bI want to\b", text, re.IGNORECASE):
            persona["Quote"] = f'"{text.strip()}"'
            persona["Citations"]["Quote"] = url

        # Age
        if match := re.search(r"\bI'?m (\d{2})\b", text):
            persona["Age"] = match.group(1)
            persona["Citations"]["Age"] = url

        # Occupation
        if "work" in text.lower() and persona["Occupation"] == "Unknown":
            persona["Occupation"] = text.strip()[:100]
            persona["Citations"]["Occupation"] = url

        # Location
        if re.search(r"\bfrom\b|\blive in\b", text, re.IGNORECASE):
            persona["Location"] = text.strip()[:100]
            persona["Citations"]["Location"] = url

        # Goals
        if re.search(r"goal|I want to|I hope", text, re.IGNORECASE):
            persona["Goals"].append((text.strip(), url))

        # Frustrations
        if re.search(r"annoyed|hate|frustrated|confusing", text, re.IGNORECASE):
            persona["Frustrations"].append((text.strip(), url))

        # Behaviours
        if re.search(r"I usually|I often|I tend to", text, re.IGNORECASE):
            persona["Behaviours"].append((text.strip(), url))

    return persona

def save_persona_to_file(persona, filename="user_persona.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{persona['Name']} - Reddit User Persona\n")
        f.write("-" * 40 + "\n")
        f.write(f"Age: {persona['Age']}")
        if "Age" in persona["Citations"]: f.write(f"  ↪ {persona['Citations']['Age']}")
        f.write("\n")

        f.write(f"Occupation: {persona['Occupation']}")
        if "Occupation" in persona["Citations"]: f.write(f"  ↪ {persona['Citations']['Occupation']}")
        f.write("\n")

        f.write(f"Location: {persona['Location']}")
        if "Location" in persona["Citations"]: f.write(f"  ↪ {persona['Citations']['Location']}")
        f.write("\n")

        f.write(f"Status: {persona['Status']}\n")
        f.write(f"Tier: {persona['Tier']}\n")
        f.write(f"Archetype: {persona['Archetype']}\n\n")

        f.write(f"Quote: {persona['Quote']}\n")
        if "Quote" in persona["Citations"]: f.write(f"  ↪ {persona['Citations']['Quote']}\n")

        f.write("\n--- Goals & Needs ---\n")
        for goal, url in persona["Goals"]:
            f.write(f"• {goal}\n  ↪ {url}\n")

        f.write("\n--- Frustrations ---\n")
        for frustration, url in persona["Frustrations"]:
            f.write(f"• {frustration}\n  ↪ {url}\n")

        f.write("\n--- Behaviours & Habits ---\n")
        for behaviour, url in persona["Behaviours"]:
            f.write(f"• {behaviour}\n  ↪ {url}\n")

    print(f"✅ Persona saved to {filename}")

def main():
    reddit_url = input("Enter Reddit profile URL: ").strip()
    match = re.search(r"reddit\.com/user/([^/]+)/?", reddit_url)
    if not match:
        print("❌ Invalid Reddit URL")
        return

    username = match.group(1)
    print(f"🔍 Fetching data for u/{username}...")
    data = scrape_user_data(username)
    persona = build_persona(data, username)
    save_persona_to_file(persona)

if __name__ == "__main__":
    main()
