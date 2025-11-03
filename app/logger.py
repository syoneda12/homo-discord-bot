import logging
import os
import sys

def setup_logger():
    log_dir = os.path.join(os.getcwd(), "app", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "bot.log")

    logger = logging.getLogger("HomoDiscordBot")

    # --- 環境変数でログレベル制御 ---
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    if logger.handlers:
        return logger

    # --- ファイル出力 ---
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # --- コンソール出力（Docker logs用） ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Logger initialized (level={log_level_str}) → {log_path}")
    return logger