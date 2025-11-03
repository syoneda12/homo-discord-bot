from datetime import datetime, timedelta

# ユーザーごとの直近通知履歴
_last_presence_state = {}
DUPLICATE_WINDOW_SECONDS = 10

# 挫折したけど一応載せておく
def register_status_events(client, config, logger):
    @client.event
    async def on_presence_update(before, after):
        try:
            now = datetime.utcnow() + timedelta(hours=9)

            before_status = str(before.status)
            after_status = str(after.status)

            # アクティビティ（ゲームやSpotifyなど）も比較
            before_activities = [a.name for a in before.activities if hasattr(a, "name")]
            after_activities = [a.name for a in after.activities if hasattr(a, "name")]

            logger.debug(
                f"[PresenceEvent] {after.name}: before={before_status} ({before_activities}) → after={after_status} ({after_activities})"
            )

            # --- ステータスもアクティビティも変わらなければ無視 ---
            if before_status == after_status and before_activities == after_activities:
                return

            # --- 重複通知防止 ---
            current_state = (before_status, after_status, tuple(after_activities))
            now_utc = datetime.utcnow()
            last_entry = _last_presence_state.get(after.id)
            if last_entry:
                last_state, last_time = last_entry
                if (
                    last_state == current_state
                    and (now_utc - last_time).total_seconds() < DUPLICATE_WINDOW_SECONDS
                ):
                    logger.debug(f"[Skip Duplicate] {after.name}: {current_state}")
                    return

            _last_presence_state[after.id] = (current_state, now_utc)

            # --- 通知チャンネル解決 ---
            channel_id = config["USER_STATUS_MAP"].get(after.id)
            if channel_id is None:
                channel_id = config["TEXT_CHANNEL_ID_DEFAULT_STATUS_CHANGE_NOTIFICATION"]
            if not channel_id:
                return

            bot_room = client.get_channel(channel_id)
            if bot_room is None:
                try:
                    bot_room = await client.fetch_channel(channel_id)
                except Exception as e:
                    logger.warning(f"fetch_channel failed: {channel_id} {e}")
                    return

            msg = (
                f"**{after.name}** が `{before_status}` → `{after_status}` になりました。 "
                f"({now:%m/%d %H:%M:%S})"
            )
            await bot_room.send(msg)
            logger.info(f"[Presence Notify] {msg}")

        except Exception as e:
            logger.error(f"Error in on_presence_update: {e}", exc_info=True)
