import asyncio
import datetime
import logging
import time

import pytest

from tghandler.handler import TelegramLoggingHandler


@pytest.fixture()
def mocked_handler():
    messages = []
    handler = TelegramLoggingHandler("token", [1, 2])
    handler.send2telegram = lambda msg: messages.append(msg)
    handler.format = lambda rec: rec.msg
    return messages, handler


async def test_emit_handler(mocked_handler):
    messages, handler = mocked_handler

    record = logging.LogRecord("test", 10, ".", 12, "test_log", (), None)
    record.created = 1685254391

    handler.emit(record)
    await asyncio.sleep(0.01)  # for unblock event loop
    assert len(messages) == 2
    assert messages[0]["chat_id"] in (1, 2)
    assert messages[1]["chat_id"] in (1, 2)
    right_message = "test_log\ntime: 2023-05-28 09:13:11 \nlevel: DEBUG\n"
    assert messages[0]["text"] == right_message
    assert messages[1]["text"] == right_message
