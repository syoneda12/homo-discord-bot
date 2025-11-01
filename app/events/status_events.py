
from datetime import datetime, timedelta

# ステータス変更通知は挫折したけど一応残しとく
def register_status_events(client, config, logger):
    # presence更新時に呼ばれる（online/idle/dnd/offline等の変更）
    @client.event
    async def on_presence_update(before, after):
        try:
            # before/after は Member オブジェクト
            if str(before.status) == str(after.status):
                return  # 変更なし

            now = datetime.utcnow() + timedelta(hours=9)
            # どのチャンネルに投稿するかをIDから取得（未キャッシュ時はfetch）
            async def resolve_channel(channel_id):
                ch = client.get_channel(channel_id)
                if ch is None:
                    try:
                        ch = await client.fetch_channel(channel_id)
                    except Exception as e:
                        logger.warning(f"fetch_channel failed: {channel_id} {e}")
                return ch

            # 対象ユーザ別の通知先を切替
            if after.id == config["OSSAN_ID"]:
                bot_room = await resolve_channel(config["TEXT_CHANNEL_ID_OSSAN_STATUS_CHANGE_NOTIFICATION"])
                if bot_room:
                    await bot_room.send(f"{after.status.name} `({now:%m/%d %H:%M:%S})`")

            elif after.id == config["TWINBIRD_ID"]:
                bot_room = await resolve_channel(config["TEXT_CHANNEL_ID_TWINBIRD_STATUS_CHANGE_NOTIFICATION"])
                if bot_room:
                    await bot_room.send(f"**{after.name}** が `{after.status.name}` になりました。 ({now:%m/%d %H:%M:%S})")

            else:
                bot_room = await resolve_channel(config["TEXT_CHANNEL_ID_OTHER_STATUS_CHANGE_NOTIFICATION"])
                if bot_room:
                    await bot_room.send(f"**{after.name}** が `{after.status.name}` になりました。 ({now:%m/%d %H:%M:%S})")

            logger.debug(f"Presence changed: {after} -> {after.status} (guild={after.guild.name})")

        except Exception as e:
            logger.error(f"Error in on_presence_update: {e}")
