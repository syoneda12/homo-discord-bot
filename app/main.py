import asyncio
import discord
from app.config import load_config
from app.logger import setup_logger
from app.events.voice_events import register_voice_events
from app.events.status_events import register_status_events

logger = setup_logger()
config = load_config()

intents = discord.Intents.default()
intents.guilds = True
intents.members = True           # ✅ Server Members Intent (有効化必須)
intents.presences = True         # ✅ Presence Intent (有効化必須)
intents.voice_states = True

client = discord.Client(intents=intents)

# 監視用チャンネルを起動時に解決（未キャッシュ対策）
CHANNEL_IDS_TO_PREFETCH = set()
CHANNEL_IDS_TO_PREFETCH.add(config["VOICE_NOTIFICATION_CHANNEL"])
CHANNEL_IDS_TO_PREFETCH.update(config["USER_STATUS_MAP"].values())
if config["TEXT_CHANNEL_ID_DEFAULT_STATUS_CHANGE_NOTIFICATION"]:
    CHANNEL_IDS_TO_PREFETCH.add(config["TEXT_CHANNEL_ID_DEFAULT_STATUS_CHANGE_NOTIFICATION"])
CHANNEL_IDS_TO_PREFETCH = list(CHANNEL_IDS_TO_PREFETCH)

@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user} (ID: {client.user.id})")
    logger.info(f"Connected guilds: {[g.name for g in client.guilds]}")

    for guild in client.guilds:
        try:
            logger.info(f"Chunking guild: {guild.name} ({guild.id}) members={guild.member_count}")
            await guild.chunk()
            logger.info(f"✅ Chunk complete: {guild.name} ({guild.id})")

            # --- キャッシュ安定化のため数秒待機 ---
            await asyncio.sleep(5)
            cached_count = len(guild.members)
            logger.info(f"Guild cache stabilized: {guild.name} ({guild.id}) cached_members={cached_count}")

        except Exception as e:
            logger.warning(f"⚠ guild.chunk() failed for {guild.name}: {e}")

    # --- チャンネルプリフェッチ ---
    for ch_id in CHANNEL_IDS_TO_PREFETCH:
        try:
            ch = client.get_channel(ch_id)
            if ch is None:
                ch = await client.fetch_channel(ch_id)
            logger.info(f"Prefetched channel: {ch} ({ch_id})")
        except Exception as e:
            logger.warning(f"Failed to prefetch channel {ch_id}: {e}")

    logger.info("Bot initialization complete. Waiting for events...")

# --- イベント登録 ---
register_voice_events(client, config, logger)
register_status_events(client, config, logger)

client.run(config["DISCORD_BOT_TOKEN"])
