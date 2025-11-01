
import discord
from app.config import load_config
from app.logger import setup_logger
from app.events.voice_events import register_voice_events
from app.events.status_events import register_status_events

logger = setup_logger()
config = load_config()

intents = discord.Intents.default()
intents.guilds = True
intents.members = True           # Server Members Intent (portalでも有効化必須)
intents.presences = True         # Presence Intent (portalでも有効化必須)
intents.voice_states = True

client = discord.Client(intents=intents)

# 監視用チャンネルを起動時に解決（未キャッシュ対策）
CHANNEL_IDS_TO_PREFETCH = list(set([
    config["VOICE_NOTIFICATION_CHANNEL"],
    config["TEXT_CHANNEL_ID_OSSAN_STATUS_CHANGE_NOTIFICATION"],
    config["TEXT_CHANNEL_ID_TWINBIRD_STATUS_CHANGE_NOTIFICATION"],
    config["TEXT_CHANNEL_ID_OTHER_STATUS_CHANGE_NOTIFICATION"],
]))

@client.event
async def on_ready():
    logger.info(f"✅ Logged in as {client.user} (ID: {client.user.id})")
    # Guildのメンバーキャッシュを温める（presence変更イベントのため）
    for guild in client.guilds:
        try:
            await guild.chunk()   # 可能な限りメンバーをキャッシュ
            logger.info(f"Chunked guild: {guild.name} ({guild.id}), members={guild.member_count}")
        except Exception as e:
            logger.warning(f"guild.chunk() failed for {guild.name}: {e}")

    # 監視用テキストチャンネルのプリフェッチ
    for ch_id in CHANNEL_IDS_TO_PREFETCH:
        try:
            ch = client.get_channel(ch_id)
            if ch is None:
                ch = await client.fetch_channel(ch_id)
            logger.info(f"Prefetched channel: {ch} ({ch_id})")
        except Exception as e:
            logger.warning(f"Failed to prefetch channel {ch_id}: {e}")

# イベント登録
register_voice_events(client, config, logger)
register_status_events(client, config, logger)

client.run(config["DISCORD_BOT_TOKEN"])
