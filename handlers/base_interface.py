from aiogram import Router, F, types
from aiogram.filters import Command

from handlers import questions
from keyboards import main_interface
from aiogram.types import Message

router = Router()
mess = ["Фамилия Имя Отчество", "Дата рождения", "Дата смерти", ]
flag = False

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет!\n\nЯ - чат-бот, который поможет тебе заполнить профиль человека в проекте Код Памяти. \nЯ предлагаю "
        "тебе пройти небольшой тест, с помощью которого я сгенерирую текст для трудных творческих полей \n Нажмите "
        "кнопку Пройти тест для того , чтобы продолжить работу",

        reply_markup=main_interface.start()
    )
    await message.answer("")
@router.message(F.text.lower() == "пройти тест")
async def test(message: types.Message):
    await message.reply("Ответь на несколько вопросов про близкого человека:")
    flag = True

if flag:
    @router.message()
    async def with_puree(message: types.Message):
        await message.reply("Ответь на несколько вопросов про близкого человека:")
        flag = True





