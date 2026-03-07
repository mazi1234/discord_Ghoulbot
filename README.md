# discord_ghoulbot

A Discord bot that notifies a text channel when enough members join a voice channel.

## Setup

### 1. Prerequisites
- Python 3.8+
- A Discord bot token ([create one here](https://discord.com/developers/applications))
- The bot needs **Server Members Intent** and **Voice State Intent** enabled in the Developer Portal

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
```
Open `.env` and fill in your bot token:
```
DISCORD_TOKEN=your_actual_token_here
config_file=config.json
commands_file=commands.json
```

### 4. Run
```bash
python join_notif_bot.py
```

---

## Configuration (`config.json`)

| Key | Default | Description |
|-----|---------|-------------|
| `DEFAULT_TEXT_CHANNEL_NAME` | `join_notifications` | Text channel the bot posts to |
| `MIN_NUM_USERS` | `1` | Min users in VC before a notification is sent |
| `MAX_NUM_USERS` | `6` | Max users — notifications stop above this |
| `DEFAULT_GREETING` | `Hello` | Word used in the notification message |
| `DEFAULT_SLOWMODE_DELAY` | `300` | Seconds between notifications (cooldown) |
| `command_prefix` | `/` | Prefix for bot commands |

---

## Commands

Use the configured prefix (default `/`) in any text channel the bot can read.

| Command | Description |
|---------|-------------|
| `!set MIN_NUM_USERS <n>` | Set minimum users to trigger notification |
| `!set MAX_NUM_USERS <n>` | Set maximum users threshold |
| `!help` | Show all available commands |
