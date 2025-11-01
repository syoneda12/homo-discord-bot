# homo-discord-bot

## 概要
Discord サーバーの入退室・ステータス変更を監視して通知するボット。  
Dockerコンテナで常駐稼働する。

## 構成
- `app/main.py` : Botエントリーポイント
- `app/events/voice_events.py` : 入退室検知
- `app/events/status_events.py` : ステータス変化検知
- `app/config.py` : 環境変数設定
- `app/logger.py` : ログ設定
- `docker-compose.yml` : デプロイ構成

## 重要設定（必須）
1. Discord Developer Portal で以下の **Privileged Gateway Intents** を有効化：
   - SERVER MEMBERS INTENT
   - PRESENCE INTENT
2. `.env` を設定（IDはすべて整数）。
3. 再起動：`docker compose up -d --build`

## 実行方法
```bash
docker compose up -d --build
```

## 技術メモ
- 起動時に `guild.chunk()` してメンバーキャッシュを温め、presenceイベントの取りこぼしを低減。
- 監視チャンネルは `fetch_channel` フォールバックで未キャッシュ対策。