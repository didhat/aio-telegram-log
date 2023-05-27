import logging
import logging.config


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "INFO",
        "handlers": ["default", "telegram"],
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d "
            "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "telegram": {
            "class": "tghandler.handler.TelegramLoggingHandler",
            "token": "token",
            "chat_ids": [0, 1],
            "level": "ERROR",
            "formatter": "default",
        },
    },
    "loggers": {
        "tryceratops": {
            "level": "INFO",
            "handlers": ["default", "telegram"],
        },
    },
}


def init_logging_config():
    logging.config.dictConfig(LOGGING_CONFIG)


async def main():
    init_logging_config()
    logger = logging.getLogger(__name__)
    logger.error("test log")
    await asyncio.sleep(10)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
