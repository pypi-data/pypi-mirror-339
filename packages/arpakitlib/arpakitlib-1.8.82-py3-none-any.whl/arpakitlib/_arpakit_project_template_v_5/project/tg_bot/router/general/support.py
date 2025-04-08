import logging

import aiogram
from aiogram import Router
from aiogram.filters import Command, or_f

from project.tg_bot.blank.client import get_cached_client_tg_bot_blank
from project.tg_bot.const import GeneralTgBotCommands
from project.tg_bot.filter_.message_text import MessageTextTgBotFilter
from project.tg_bot.middleware.common import MiddlewareDataTgBot

tg_bot_router = Router()
_logger = logging.getLogger(__name__)


@tg_bot_router.message(
    or_f(
        Command(GeneralTgBotCommands.support),
        MessageTextTgBotFilter([
            GeneralTgBotCommands.support,
            "поддержка"
        ], ignore_case=True)
    )
)
async def _(
        m: aiogram.types.Message,
        middleware_data_tg_bot: MiddlewareDataTgBot,
        **kwargs
):
    await m.answer(text=get_cached_client_tg_bot_blank().support())
