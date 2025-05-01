import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from db import load, write

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7473790618:AAFrIQ1QKZGTEkyJJ0Vowx2lsE2cT2E7G0E*"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))



dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject) -> None:
    data = load()
    data[str(message.from_user.id)] = 0
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    chat_id = command.args
    if chat_id:
        old_cnt = data.get(chat_id, 0)
        data[chat_id] = old_cnt + 1
        await message.answer(f"Siz quyidagi userga ref olgasiz {chat_id}")
    write(data)




@dp.message(Command("refer"))
async def echo_handler(message: Message) -> None:
    link = await create_start_link(bot=bot, payload=str(message.from_user.id))
    await message.answer(link)

@dp.message(Command("count"))
async def echo_handler(message: Message) -> None:
    data = load()
    chat_id = str(message.from_user.id)

    await message.answer(f"{data.get(chat_id, 0)}")

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls


    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())