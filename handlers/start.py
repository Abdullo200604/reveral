from aiogram import Router, html
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.deep_linking import create_start_link

from db import add_user_if_not_exists, increment_referral

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject):
    user_id = str(message.from_user.id)
    add_user_if_not_exists(user_id)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Referla")],
            [KeyboardButton(text="Referallar soni")]
        ],
        resize_keyboard=True
    )

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=keyboard)

    referrer_id = command.args
    if referrer_id and referrer_id != user_id:
        add_user_if_not_exists(referrer_id)
        increment_referral(referrer_id)
        await message.answer(f"Siz quyidagi userga refer bo‘ldingiz: {referrer_id}")
    elif referrer_id == user_id:
        await message.answer("Siz o‘zingizga refer bo‘la olmaysiz.")