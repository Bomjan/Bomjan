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

cards = []
for repo in repos[:3]:
    name = repo["name"]
    url = repo["html_url"]
    pushed_at = repo["pushed_at"][:10]

    pin_url = (
        "https://github-readme-stats.vercel.app/api/pin/"
        f"?username={USERNAME}&repo={name}"
        "&hide_border=true&bg_color=FBF3EA&title_color=4A3526"
        "&text_color=6B4F3F&icon_color=C17F59"
    )

    cards.append(f"""<a href="{url}">
  <img src="{pin_url}" alt="{name}" />
</a>
<br/>
<sub>Last activity: {pushed_at}</sub>""")

block = "<div align=\"center\">\n\n" + "\n\n".join(cards) + "\n\n</div>"

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
