name: Blitz Discord Sync

on:
  schedule:
    - cron: "*/10 * * * *"   # every 10 minutes (GitHub may delay a few minutes)
  workflow_dispatch:          # lets you run it manually from the Actions tab

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install requests
      - run: python sync_discord.py
        env:
          DISCORD_TOKEN: ${{ secrets.DISCORD_TOKEN }}
          WEBAPP_URL: ${{ secrets.WEBAPP_URL }}
          RELAY_SECRET: ${{ secrets.RELAY_SECRET }}
name: Blitz Discord Sync

on:
  schedule:
    - cron: "*/10 * * * *"   # every 10 minutes (GitHub may delay a few minutes)
  workflow_dispatch:          # lets you run it manually from the Actions tab

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install requests
      - run: python sync_discord.py
        env:
          DISCORD_TOKEN: ${{ secrets.DISCORD_TOKEN }}
          WEBAPP_URL: ${{ secrets.WEBAPP_URL }}
          RELAY_SECRET: ${{ secrets.RELAY_SECRET }}
