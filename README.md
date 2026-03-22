# Telegram Claude Bot

A Telegram bot powered by Claude AI (Anthropic), deployed as a serverless Python function on Vercel.

## Features
- Chat with Claude directly from Telegram
- Per-user conversation history (last 20 messages)
- `/start`, `/clear`, `/help` commands
- Serverless — zero cost on Vercel hobby plan for moderate usage

## Setup
See `TODO.md` — open the project folder with Claude CLI and it will guide you through everything automatically.

## Architecture
```
Telegram User
     │
     ▼
Telegram Servers
     │  POST /webhook
     ▼
Vercel Serverless Function (api/webhook.py)
     │
     ▼
Anthropic Claude API
     │
     ▼
Reply sent back to user via Telegram API
```

## Environment Variables
| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | From console.anthropic.com |
| `TELEGRAM_BOT_TOKEN` | From @BotFather on Telegram |

## Commands
| Command | Action |
|---|---|
| `/start` | Start or restart the bot |
| `/clear` | Clear conversation history |
| `/help` | Show help message |
