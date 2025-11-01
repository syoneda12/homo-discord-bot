
from datetime import datetime, timedelta

def register_voice_events(client, config, logger):
    @client.event
    async def on_voice_state_update(member, before, after):
        try:
            if before.channel == after.channel:
                return
            now = datetime.utcnow() + timedelta(hours=9)
            # 通知メッセージを書き込むテキストチャンネル（チャンネルIDを指定）
            bot_room = client.get_channel(config["VOICE_NOTIFICATION_CHANNEL"])
            if bot_room is None:
                try:
                    bot_room = await client.fetch_channel(config["VOICE_NOTIFICATION_CHANNEL"])
                except Exception as e:
                    logger.warning(f"Failed to resolve VOICE_NOTIFICATION_CHANNEL: {e}")
                    return
            # メッセージを送信
            if before.channel and before.channel.id in config["VOICE_CHANNELS"]:
                await bot_room.send(f'▲ **{member.display_name}** が `{before.channel.name}` から退出しました ({now:%m/%d %H:%M:%S})')
            if after.channel and after.channel.id in config["VOICE_CHANNELS"]:
                await bot_room.send(f'▼ **{member.display_name}** が `{after.channel.name}` に参加しました ({now:%m/%d %H:%M:%S})')
        except Exception as e:
            logger.error(f"Error in on_voice_state_update: {e}")
