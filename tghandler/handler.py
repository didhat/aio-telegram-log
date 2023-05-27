import asyncio
import aiohttp
import logging
import datetime

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
        text = self.record2tg(record)

        loop = asyncio.get_event_loop()
        loop.create_task(self.send_message(text))

    def record2tg(self, record: logging.LogRecord):
        msg = self.format(record)
        return f"{msg}\ntime: {datetime.datetime.fromtimestamp(record.created)} \nlevel: {record.levelname}\n"

    def format_url(self, method: str):
        return f"{self.telegram_url}/bot{self._token}/{method}"

    async def send_message(self, text: str):
        send = self.get_message_sender(text)

        await asyncio.gather(*[send(ch_id) for ch_id in self._chat_ids])

    def get_message_sender(self, text: str):
        message = {"text": text}

        async def sender(chat_id: int):
            if self.session is None:
                logger.warning("can not send logs to telegram because session is None")

            message["chat_id"] = chat_id
            try:
                response = await self.send2telegram(message)
            except Exception as e:
                logger.warning(f"can not send message to telegram: {e}")
                return
            return response

        return sender

    async def send2telegram(self, message: dict):
        async with self.session.post(
            self.format_url("sendMessage"), json=message
        ) as resp:
            return resp
