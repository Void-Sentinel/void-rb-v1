# Void Sentinel

A Discord slash-command bot built for **raid / spam operations** (formerly "Void Spam Bot", v2.0.5). It ships a set of slash commands and interactive button-based utilities for mass-messaging, ghost pinging, fake giveaways, and custom message presets.

> ⚠️ This tool is intended for educational / authorized testing purposes only. Mass-mentioning, spamming, and ghost-pinging other servers without permission may violate Discord's [Terms of Service](https://discord.com/terms) and can get the bot and account banned. Use responsibly and only where you have permission.

---

## Features

| Command | Description |
| --- | --- |
| `/r4id [preset]` | The main raid command. Sends the configured `RAID_MESSAGE` (or a saved preset) 5x via a button-triggered webhook spam. |
| `/ghostping [user]` | Pings `@everyone` or a specific user, then immediately deletes the message (ghost ping). |
| `/fakegiveaway [prize]` | Posts a fake giveaway embed with a "Claim" button that spams a `@everyone` raid message when clicked. |
| `/custom-msg` | Premium preset manager: create / list / delete custom raid message presets (stored in SQLite). |
| `/blame [user]` | Posts a fake "Raid Complete" embed blaming a user with a random completion time. |
| `/say <message>` | Makes the bot repeat a message. |
| `/botinfo` | Shows loaded cogs, command count, and bot metadata. |

All slash commands are synced globally on startup and work in guilds, DMs, and private channels.

---

## Project Structure

```
Void Sentinel Raid/
├── main.py                 # Entry point, bot setup, auto-loads cogs, syncs commands
├── requirements.txt        # Python dependencies
├── core/
│   ├── config.py           # Live config (TOKEN, RAID_MESSAGE, etc.)
│   ├── config.example.py   # Example config to copy
│   ├── utils.py            # Discord webhook send/delete helpers
│   └── logger.py           # Logging utilities
├── cogs/
│   ├── raid/               # raid, ghostping, giveaway, custom, blame, say
│   └── utils/              # botinfo
└── data/
    └── presets.db          # SQLite database for custom message presets (auto-created)
```

---

## Requirements

- Python 3.10+
- A Discord bot token with the **Message Content** intent enabled
- The following Python packages (add to `requirements.txt`):

```txt
discord.py>=2.0
aiosqlite
aiohttp
```

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd "Void Sentinel Raid"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   Copy the example config and fill in your token:
   ```bash
   cp core/config.example.py core/config.py
   ```
   Then edit `core/config.py`:
   ```python
   TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
   COMMAND_LOG_CHANNEL_ID = 1531986215157497907
   DEBUG_MODE = 0
   RAID_MESSAGE = """
   # > FUCKED BY [VOID SENTINEL](https://discord.gg/Zwa2Jx6vf7)
   # YALL NEED BETTER SECURITY @everyone
   """
   ```

4. **Create the Discord application**
   - Create a bot at the [Discord Developer Portal](https://discord.com/developers/applications)
   - Enable the **Message Content Intent** under Bot → Privileged Gateway Intents
   - Invite it to your server with `applications.commands` and `Send Messages` scopes

---

## Running

```bash
python main.py
```

On startup the bot:
- Loads every module under `cogs/` automatically
- Syncs all slash commands globally
- Prints loaded extensions and the number of synced commands

---

## Configuration Reference (`core/config.py`)

| Variable | Purpose |
| --- | --- |
| `TOKEN` | Discord bot token. |
| `COMMAND_LOG_CHANNEL_ID` | Channel ID used for command logging. |
| `DEBUG_MODE` | Toggle debug behavior (0 = off). |
| `RAID_MESSAGE` | Default message sent by `/r4id`. Supports Markdown / mentions. |

---

## How It Works

- **Message spam** uses Discord's interaction webhook (`/webhooks/{app_id}/{token}`) directly via `aiohttp`, bypassing rate-light gateway sends and firing 5 messages per button press.
- **Presets** are persisted per-user in `data/presets.db` (SQLite via `aiosqlite`) and can be referenced by name in `/r4id`.
- **Ghost ping** sends a mention over the interaction webhook then deletes it, leaving only a notification in the target's inbox.

---

## Notes

- Custom presets (`/custom-msg`) are gated with a `[PREMIUM]` label in their description.
- The bot currently has no built-in permission checks — any user who can invoke slash commands can use every feature. Add role/permission guards before deploying publicly.
- Developed by **Voby7**. Join the community: https://discord.gg/Zwa2Jx6vf7

---

## Disclaimer

This software is provided as-is for authorized security testing and educational use. The author is not responsible for any misuse, ToS violations, or bans resulting from its use.
