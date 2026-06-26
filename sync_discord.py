"""
BLITZ LEAGUE — Discord relay
Runs on GitHub Actions (servers Discord does NOT block). Reads the three
channels and forwards new messages to the sheet's Web App, which writes them.

Secrets come from GitHub repo settings (Settings > Secrets and variables > Actions):
  DISCORD_TOKEN   - your Discord bot token
  WEBAPP_URL      - the Apps Script Web app URL
  RELAY_SECRET    - the same random string you put in the sheet's Script properties
"""
import os
import requests

TOKEN = os.environ["DISCORD_TOKEN"]
WEBAPP_URL = os.environ["WEBAPP_URL"]
SECRET = os.environ["RELAY_SECRET"]

CHANNELS = {
    "highlights": "1519910954635231343",
    "scores":     "1519910992203485215",
    "trash":      "1519911020301127700",
}

API = "https://discord.com/api/v10"


def fetch(channel_id):
    r = requests.get(
        f"{API}/channels/{channel_id}/messages?limit=50",
        headers={"Authorization": f"Bot {TOKEN}"},
        timeout=30,
    )
    r.raise_for_status()
    out = []
    for m in r.json():
        author = m.get("author") or {}
        if author.get("bot"):
            continue
        out.append({
            "id": m["id"],
            "author": author.get("username", ""),
            "content": m.get("content", ""),
            "timestamp": m.get("timestamp", ""),
        })
    return out


def main():
    payload = {"secret": SECRET, "channels": {}}
    for kind, cid in CHANNELS.items():
        try:
            msgs = fetch(cid)
            payload["channels"][kind] = msgs
            print(f"{kind}: fetched {len(msgs)} message(s)")
        except Exception as ex:
            print(f"{kind}: ERROR fetching from Discord -> {ex}")
            payload["channels"][kind] = []

    res = requests.post(WEBAPP_URL, json=payload, timeout=60)
    print("Sheet receiver responded:", res.status_code)
    print(res.text[:800])


if __name__ == "__main__":
    main()
