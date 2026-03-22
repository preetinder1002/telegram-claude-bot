# TODO: Telegram Claude Bot — End-to-End Setup

> This file is meant to be opened with Claude CLI (Claude Code).
> Run `claude` in this folder and say: "Follow the TODO.md and set everything up for me."
> Claude CLI will execute all steps automatically.

---

## Prerequisites Check

Before starting, verify these tools are installed:

```
CHECK: Run these commands and confirm they succeed:
- git --version
- gh --version         (GitHub CLI — install: https://cli.github.com)
- vercel --version     (Vercel CLI — install: npm install -g vercel)
- gh auth status       (must be logged in — if not: gh auth login)
- vercel whoami        (must be logged in — if not: vercel login)
```

If any are missing, install them first then come back.

---

## Step 1 — Create your .env file

1. Copy `.env.example` to `.env`:
   ```
   cp .env.example .env
   ```

2. Open `.env` and fill in:
   - `ANTHROPIC_API_KEY` → get from https://console.anthropic.com/settings/keys
   - `TELEGRAM_BOT_TOKEN` → get from Telegram by messaging @BotFather and running /newbot

   **Do not skip this step.** The bot will not work without these values.

---

## Step 2 — Initialize Git and push to GitHub

Run these commands in order:

```bash
git init
git add .
git commit -m "Initial commit: Telegram Claude bot"
gh repo create telegram-claude-bot --public --source=. --remote=origin --push
```

Expected result: A new GitHub repo created at github.com/YOUR_USERNAME/telegram-claude-bot

---

## Step 3 — Deploy to Vercel

```bash
vercel link --yes
vercel deploy --prod
```

When prompted by `vercel link`:
- Select your existing scope / team
- Confirm project name as `telegram-claude-bot`

After deploy succeeds, **copy the production URL** shown in the output.
It will look like: `https://telegram-claude-bot-xxxx.vercel.app`

---

## Step 4 — Set Environment Variables on Vercel

Run these two commands (replace with your actual values from .env):

```bash
vercel env add ANTHROPIC_API_KEY production
vercel env add TELEGRAM_BOT_TOKEN production
```

Each command will prompt you to paste the value. Paste from your `.env` file.

Then redeploy to apply the env vars:

```bash
vercel deploy --prod
```

---

## Step 5 — Register Telegram Webhook

Replace `YOUR_BOT_TOKEN` and `YOUR_VERCEL_URL` and run:

```bash
curl "https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook?url=YOUR_VERCEL_URL/webhook"
```

Example:
```bash
curl "https://api.telegram.org/bot123456:ABC-DEF/setWebhook?url=https://telegram-claude-bot-xxxx.vercel.app/webhook"
```

Expected response:
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

---

## Step 6 — Verify Everything Works

1. Open Telegram and search for your bot by the username you gave @BotFather
2. Send `/start`
3. You should get: "Hi! I'm Claude. Ask me anything."
4. Send any message — Claude should respond within a few seconds

---

## Step 7 — Connect GitHub to Vercel (auto-deploys)

```bash
vercel git connect
```

This links your GitHub repo so every push to `main` auto-deploys to Vercel.

---

## Done!

Your bot is live. Summary of what was set up:
- GitHub repo: github.com/YOUR_USERNAME/telegram-claude-bot
- Vercel deployment: https://telegram-claude-bot-xxxx.vercel.app
- Telegram webhook: registered and active
- Auto-deploy: every push to main triggers a new Vercel deploy

---

## Troubleshooting

**Bot not responding?**
```bash
# Check webhook is set correctly
curl "https://api.telegram.org/botYOUR_BOT_TOKEN/getWebhookInfo"

# Check Vercel runtime logs
vercel logs --prod
```

**Env vars not working?**
```bash
vercel env ls
```

**Redeploy from scratch:**
```bash
vercel deploy --prod --force
```
