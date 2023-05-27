import asyncio
import aiohttp
import logging

from typing import Optional, Final


logger = logging.getLogger(__name__)


class TelegramLoggingHandler(logging.Handler):
    telegram_url: Final = "https://api.telegram.org"

    def __init__(
        self,
        token: str,
        chat_ids: list[int],
        level: int = logging.NOTSET,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        super().__init__(level)

        self._token = token
        self._chat_ids = chat_ids

        self.lock = None  # for sending message we do not need lock
        self.session = None
        self.set_session(session)

    def set_session(self, session: Optional[aiohttp.ClientSession]):
        if session is None:
            self.session = aiohttp.ClientSession()
        else:
            self.session = session

    def emit(self, record: logging.LogRecord) -> None:
        text = self.format(record)
        loop = asyncio.get_running_loop()
        loop.run_until_complete(self.send_message(text))

    def format_url(self, method: str):
        return f"{self.telegram_url}/bot{self._token}/{method}"

    async def send_message(self, text: str):
        if self.session is None:
            logger.warning("can not send logs to telegram due to session is None")
            return
        send = self.get_message_sender(text)

        await asyncio.gather(*[send(ch_id) for ch_id in self._chat_ids])

    def get_message_sender(self, text: str):
        message = {"text": text}

        async def sender(chat_id: int):
            message["chat_id"] = chat_id
            try:
                async with self.session.post(
                    self.format_url("sendMessage"), json=message
                ) as resp:
                    return await resp.json()
            except Exception as e:
                logger.warning(f"can not send message to telegram: {e}")

        return sender
