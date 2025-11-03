
import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()

    # --- 可変ボイスチャンネル設定 ---
    voice_channel_ids = [
        int(ch_id.strip())
        for ch_id in os.getenv("HOMOSERVER_VOICEC_IDS", "").split(",")
        if ch_id.strip().isdigit()
    ]

    # --- ステータス監視対象マップ ---
    user_status_map_env = os.getenv("USER_STATUS_MAP", "")
    user_status_map = {}
    for pair in user_status_map_env.split(","):
        if ":" in pair:
            uid, chid = pair.split(":", 1)
            if uid.strip().isdigit() and chid.strip().isdigit():
                user_status_map[int(uid.strip())] = int(chid.strip())

    return {
        "DISCORD_BOT_TOKEN": os.getenv("DISCORD_BOT_TOKEN"),
        "VOICE_NOTIFICATION_CHANNEL": int(os.getenv("HOMOSERVER_TEXTC_VOICE_CHANNEL_NOTIFICATION")),
        "VOICE_CHANNELS": voice_channel_ids,
        "USER_STATUS_MAP": user_status_map,
        "TEXT_CHANNEL_ID_DEFAULT_STATUS_CHANGE_NOTIFICATION": int(
            os.getenv("TEXT_CHANNEL_ID_DEFAULT_STATUS_CHANGE_NOTIFICATION", "0")
        ) or None,
    }