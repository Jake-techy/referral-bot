import os, feedparser
from jinja2 import Environment, FileSystemLoader
from telegram import Bot
from dotenv import load_dotenv

# ── 1. Load secrets from .env ────────────────────────────
load_dotenv()                                   # reads .env file in this folder
TG_TOKEN = os.getenv("TG_BOT_TOKEN")            # your Telegram bot token
TG_CHAT  = os.getenv("TG_CHAT_ID")               # your Telegram chat ID
tg = Bot(TG_TOKEN) if TG_TOKEN else None        # create Bot object if configured

# ── 2. Prepare the HTML template ───────────────────────
env  = Environment(loader=FileSystemLoader("templates"))
tmpl = env.get_template("offers.html")           # looks for templates/offers.html

# ── 3. Fetch referral offers from RSS ──────────────────
def fetch_offers():
    # ── TEST DATA: forces HTML to change each run
    from datetime import datetime
    return [{
        "title": f"TEST OFFER at {datetime.utcnow().isoformat()}",
        "link":  "https://example.com"
    }]

# ── 4. Render HTML + send Telegram alert ───────────────
def publish():
    offers = fetch_offers()                      # get latest offers
    html   = tmpl.render(offers=offers)          # fill template with data

    # ensure the output folder exists
    os.makedirs("docs", exist_ok=True)
    # write HTML page
    with open("docs/index.html", "w") as f:
        f.write(html)

    # if Telegram is set up, send the top 5 offers
    if tg:
        msg = "\n".join(f"[{o['title']}]({o['link']})" for o in offers[:5])
        tg.send_message(chat_id=TG_CHAT, text=msg, parse_mode="Markdown")

# ── 5. Run publish() when this script is executed ───────
if __name__ == "__main__":
    publish()
