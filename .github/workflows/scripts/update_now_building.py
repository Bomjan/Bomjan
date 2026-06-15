import os
import re
import urllib.request
import json

USERNAME = "Bomjan"
PROFILE_REPO = "Bomjan"
TOKEN = os.environ.get("GITHUB_TOKEN")
README_PATH = "README.md"


def fetch(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-readme-bot",
    })
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


repos = fetch(f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&per_page=10")
repos = [r for r in repos if not r["fork"] and r["name"] != PROFILE_REPO]

latest = repos[0]
name = latest["name"]
description = latest["description"] or "No description provided."
url = latest["html_url"]
pushed_at = latest["pushed_at"][:10]

block = f"""<div align="center">

**{name}**

{description}

*Last updated: {pushed_at}*

[View Project →]({url})

</div>"""

with open(README_PATH, "r") as f:
    content = f.read()

content = re.sub(
    r"<!--NOW_BUILDING:START-->.*?<!--NOW_BUILDING:END-->",
    f"<!--NOW_BUILDING:START-->\n{block}\n<!--NOW_BUILDING:END-->",
    content,
    flags=re.DOTALL,
)

with open(README_PATH, "w") as f:
    f.write(content)
