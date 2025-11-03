# homo-discord-bot

## 概要
Discord サーバーの **ボイスチャンネル入退室** と **ユーザーステータス（オンライン／退席／オフラインなど）** を監視し、
指定したテキストチャンネルに自動通知するボットです。
Docker コンテナで常駐稼働できます。

## 主な特徴
- 複数ボイスチャンネルを可変で監視可能
- ユーザーごとに異なる通知チャンネルを設定可能
- ステータス変更を精密に検知（online / idle / dnd / offline）
- 短時間の重複通知を自動抑止（デバウンス機能）
- ログを Docker 標準出力とファイルの両方に出力

## 実行方法
```bash
cp .env.template .env.development
docker compose up -d --build
docker logs -f homo-discord-bot
```

## .env 設定例
```env
DISCORD_BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HOMOSERVER_TEXTC_VOICE_CHANNEL_NOTIFICATION=111111111111111111
HOMOSERVER_VOICEC_IDS=222222222222222222,333333333333333333
USER_STATUS_MAP=444444444444444444:555555555555555555,666666666666666666:777777777777777777
TEXT_CHANNEL_ID_DEFAULT_STATUS_CHANGE_NOTIFICATION=888888888888888888
LOG_LEVEL=DEBUG
```

## ファイル構成
- app/config.py : 設定ロード
- app/logger.py : ログ設定（ファイル＋Docker出力）
- app/main.py : エントリーポイント（チャンク安定化付き）
- app/events/status_events.py : ステータス監視
- app/events/voice_events.py : ボイス監視

## ライセンス
MIT License