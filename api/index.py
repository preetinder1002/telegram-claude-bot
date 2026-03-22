from flask import Flask, request, jsonify
import json
import os
import anthropic
import urllib.request

app = Flask(__name__)

ANTHROPIC_KEY  = os.environ.get("ANTHROPIC_API_KEY", "")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

# In-memory conversation history per user
# Note: resets on cold start — upgrade to Redis/Upstash for persistence
histories = {}


def send_telegram(chat_id, text):
    url  = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text}).encode()
    req  = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)


@app.route("/api/webhook", methods=["POST"])
def webhook():
    body    = request.get_json(force=True)
    message = body.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text    = message.get("text", "")

    if not chat_id or not text:
        return "OK", 200

    if text == "/start":
        histories[chat_id] = []
        send_telegram(chat_id, "👋 Hi! I'm Claude. Ask me anything.")

    elif text == "/clear":
        histories[chat_id] = []
        send_telegram(chat_id, "🗑️ Conversation cleared. Fresh start!")

    elif text == "/help":
        send_telegram(chat_id,
            "Commands:\n"
            "/start - start or restart\n"
            "/clear - clear conversation history\n"
            "/help  - show this message\n\n"
            "Just type anything to chat with Claude!"
        )

    else:
        histories.setdefault(chat_id, [])
        histories[chat_id].append({"role": "user", "content": text})

        # Keep last 20 messages to avoid token overflow
        if len(histories[chat_id]) > 20:
            histories[chat_id] = histories[chat_id][-20:]

        try:
            resp  = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=histories[chat_id],
            )
            reply = resp.content[0].text
            histories[chat_id].append({"role": "assistant", "content": reply})
            send_telegram(chat_id, reply)

        except Exception as e:
            send_telegram(chat_id, f"Error: {e}")

    return "OK", 200


@app.route("/api/webhook", methods=["GET"])
def health():
    return "Telegram Claude Bot is live!", 200
