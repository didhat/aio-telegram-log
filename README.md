# Aio-telegram-log

Basic library for sending log to telegram, using python logging module(like handler), but do it asynchronously.

## Usage

Just set telegram handler in your logging settings

    ...
    "handlers": {
        "default": {
            "formatter": "default",
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "telegram": {
            "class": "tghandler.handler.TelegramLoggingHandler",
            "token": "input your token",
            "chat_ids": [0, 1],
            "level": "ERROR",
            "formatter": "default",
        },
    },
    ...


