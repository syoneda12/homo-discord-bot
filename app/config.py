
import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        "DISCORD_BOT_TOKEN": os.getenv("DISCORD_BOT_TOKEN"),
        "VOICE_NOTIFICATION_CHANNEL": int(os.getenv("HOMOSERVER_TEXTC_VOICE_CHANNEL_NOTIFICATION")),
        "VOICE_CHANNELS": [
            int(os.getenv("HOMOSERVER_VOICEC_ROBY")),
            int(os.getenv("HOMOSERVER_VOICEC_GAMING")),
        ],
        "TEXT_CHANNEL_ID_OSSAN_STATUS_CHANGE_NOTIFICATION": int(os.getenv("TEXT_CHANNEL_ID_OSSAN_STATUS_CHANGE_NOTIFICATION")),
        "TEXT_CHANNEL_ID_TWINBIRD_STATUS_CHANGE_NOTIFICATION": int(os.getenv("TEXT_CHANNEL_ID_TWINBIRD_STATUS_CHANGE_NOTIFICATION")),
        "TEXT_CHANNEL_ID_OTHER_STATUS_CHANGE_NOTIFICATION": int(os.getenv("TEXT_CHANNEL_ID_OTHER_STATUS_CHANGE_NOTIFICATION")),
        "OSSAN_ID": int(os.getenv("OSSAN_ID")),
        "TWINBIRD_ID": int(os.getenv("TWINBIRD_ID")),
    }
