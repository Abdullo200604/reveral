from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from db import get_user_referrals

router = Router()


@router.message(Command("refer"))
async def refer_handler(message: Message):
    link = await create_start_link(bot=message.bot, payload=str(message.from_user.id))
    await message.answer(link)


@router.message(Command("count"))
async def count_handler(message: Message):
    user_id = str(message.from_user.id)
    count = get_user_referrals(user_id)
    await message.answer(f"Sizga {count} ta referal bor.")