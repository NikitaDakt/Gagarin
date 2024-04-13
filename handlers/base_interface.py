from aiogram import Router, F, types
from aiogram.filters import Command

from handlers import questions
from keyboards import main_interface
from aiogram.types import Message

router = Router()

mess = ["Фамилия Имя Отчество", "Дата рождения", "Дата смерти", "Расскажите о нем: Где он родился?", "Где он учился?",
        "Где он умер?", "Какие у него были интересы и хобби?", "Какие книги, фильмы и музыку он предпочитал?"]
ans = []
question_index = 0
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
    global question_index, ans
    await message.reply("Ответь на несколько вопросов про близкого человека:")
    question_index = 0
    ans = []

@router.message()
async def handle_answers(message: types.Message):
    global question_index, ans
    if question_index < len(mess):
        if question_index == 0:
            name_pattern = re.compile(r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+$')
            if not name_pattern.match(message.text):
                await message.reply("Пожалуйста, введите Фамилию Имя Отчество в правильном формате, например, Иванов Иван Иванович.")
                return
        elif question_index == 1 or question_index == 2:
            date_pattern = re.compile(r'^\d{1,2}\.\d{1,2}\.\d{4}$')
            if not date_pattern.match(message.text):
                await message.reply("Пожалуйста, введите дату в правильном формате (дд.мм.гггг), например, 01.01.2000.")
                return
        ans.append(message.text)   #dadaya
        question_index += 1
        if question_index < len(mess):
            await message.reply(mess[question_index])
        else:
            await message.reply("Вопросы закончились. Ваши ответы сохранены.")


@router.message(Command("Проверить ответы"))
async def check_answers(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Очистить ответы"))

    if ans:
        response = "Ваши ответы:\n\n"
        for i, answer in enumerate(ans, 1):
            response += f"{i}. {answer}\n"
        await message.answer(response, reply_markup=keyboard)
    else:
        await message.answer("Ответы еще не были введены.")


@router.message(F.text.lower() == "Очистить ответы")
async def clear_answers(message: types.Message):
    global ans
    ans = []
    await message.answer("Ответы очищены.")