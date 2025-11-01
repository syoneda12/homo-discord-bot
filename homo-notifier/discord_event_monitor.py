import os
from datetime import datetime, timedelta

def register_events(client):
    # チャンネル入退室時の通知処理
    @client.event
    async def on_voice_state_update(member, before, after):
        try:
            # チャンネルへの入室ステータスが変更されたとき（ミュートON、OFFに反応しないように分岐）
            if before.channel != after.channel:
                now = datetime.utcnow() + timedelta(hours=9)
                botRoom = client.get_channel(int(os.getenv("HOMOSERVER_TEXTC_VOICE_CHANNEL_NOTIFICATION")))
                # 入退室を監視する対象のボイスチャンネル（チャンネルIDを指定）（ここでは「ロビー」「Gaming」）
                announceChannelIds = [
                    int(os.getenv("HOMOSERVER_VOICEC_ROBY")),
                    int(os.getenv("HOMOSERVER_VOICEC_GAMING"))
                ]
                # 退室通知
                if before.channel and before.channel.id in announceChannelIds:
                    await botRoom.send(f'▲**{member.display_name}** が `{before.channel.name}` から退出しました。 ({now:%m/%d %H:%M:%S})')
                # 入室通知
                if after.channel and after.channel.id in announceChannelIds:
                    await botRoom.send(f'▼**{member.display_name}** が `{after.channel.name}` に参加しました。 ({now:%m/%d %H:%M:%S})')
        except Exception as e:
            print(f"Error in on_voice_state_update: {e}")
    # ステータス変更通知は挫折したけど一応残しとく
    @client.event
    async def on_member_update(before, after):
        try:
            logger.debug("on_member_update start.")
            user = client.get_user(before.id)
            common_guilds = [guild for guild in client.guilds if user in guild.members]
            if common_guilds and before.guild.id == common_guilds[0].id:
                if str(before.status) != str(after.status):
                    logger.debug(f"Status changed from {before.status} to {after.status}")
                    now = datetime.utcnow() + timedelta(hours=9)
                    if after.id == OSSAN_ID :
                        logger.debug("botroom ossan")
                        botRoom = client.get_channel(TEXT_CHANNEL_ID_OSSAN_STATUS_CHANGE_NOTIFICATION)
                        await botRoom.send(after.status.name + '`(' + f'{now:%m/%d %H:%M:%S})')
                    elif after.id == TWINBIRD_ID:
                        logger.debug("botroom twinbird")
                        botRoom = client.get_channel(TEXT_CHANNEL_ID_TWINBIRD_STATUS_CHANGE_NOTIFICATION)
                        await botRoom.send('**' + after.name  + '** が `' + after.status.name + '` になりました。 (' + f'{now:%m/%d %H:%M:%S})')
                    else:
                        logger.debug("botroom other")
                        botRoom = client.get_channel(TEXT_CHANNEL_ID_OTHER_STATUS_CHANGE_NOTIFICATION)
                        await botRoom.send('**' + after.name  + '** が `' + after.status.name + '` になりました。 (' + f'{now:%m/%d %H:%M:%S})')
        except Exception as e:
            logger.error(f"Error in on_member_state_update: {e}")