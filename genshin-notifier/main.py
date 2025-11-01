import os
import discord
from dotenv import load_dotenv
import datetime
import traceback
import requests

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)
botRoom = client.get_channel(int(os.getenv("HOMOSERVER_TEXTC_TORI_NOTIFICATION")))

LOG_FILE = "log/genshin.log"

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def send_discord(message):
    try:
        botRoom.send(message)
    except Exception as e:
        log(f"Discord通知失敗: {e}")

def get_resin_status():
    try:
        COOKIE = os.getenv("GENSHIN_COOKIE")
        headers = {"Cookie": COOKIE, "User-Agent": "Mozilla/5.0"}
        response = requests.get(
            "https://sg-hk4e-api.hoyolab.com/event/sol/info?lang=ja-jp",
            headers=headers
        )
        data = response.json()
        current_resin = data['data']['resin']
        max_resin = data['data']['resin_limit']
        return f"原神の樹脂：{current_resin}/{max_resin}"
    except Exception as e:
        raise RuntimeError(f"原神API取得エラー: {e}")

def main():
    try:
        log("=== Genshin Notifier 実行開始 ===")
        status = get_resin_status()
        send_discord(f"🎮 {status}")
        log("=== 正常終了 ===")
    except Exception:
        err = traceback.format_exc()
        log("エラー発生:\n" + err)
        send_discord(f"原神通知失敗\n```{err}```")

if __name__ == "__main__":
    main()