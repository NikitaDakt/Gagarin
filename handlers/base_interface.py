from aiogram import Router, F
from aiogram.filters import Command
from keyboards import main_interface
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Давайте начнем работу",
        reply_markup=main_interface.start()
    )