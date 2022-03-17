# import telebot
# from telebot import *
from datetime import datetime
from aiogram import *
from bd import *

back = '⬅ Назад'
lunch = 12 * 60 + 15
def botik(token):
    bot = Bot(token)
    dp = Dispatcher(bot)
    @dp.message_handler(commands=['start', 'help'])
    async def keyboard(message: types.Message):
        #if len(request(f"SELECT step FROM bot_db.USERS WHERE id = {user};")) == 0:
        #     change(f"INSERT INTO bot_db.USERS (id, step, m_id) VALUES ({user}, 0, {message_bot.message_id});")
        # else:
        #     change(f"UPDATE bot_db.USERS SET m_id = {message_bot} WHERE id
        result = request(f"SELECT * FROM main;")
        buttons = [types.InlineKeyboardButton(text=row[1], callback_data=row[2]) for row in result]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await bot.send_message(message.from_user.id, "Добро пожаловать", reply_markup=keyboard)

    @dp.callback_query_handler()
    async def callback(call: types.CallbackQuery):
        user = call.from_user.id
        # message_bot = request(f"SELECT m_id FROM USERS WHERE id = {user};")[0][0]
        result = request(f"SELECT * FROM {call.data};")
        if call.data == 'teachers':
            weekday = datetime.now().weekday() + 1
            time = int(datetime.now().hour()) * 60 + int(datetime.now().minute())
            if lunch < time < lunch + 50:
                ... # ЩА ОБЕД
            else:
                ... # КАК ОБЫЧНО
            await call.message.edit_text(f"Сейчас {time / 60}:{time % 60}. {result[0]}, скорее всего в {result[1]} или {result[2:]}")
        else:
            buttons = [types.InlineKeyboardButton(text=row[1], callback_data=row[2]) for row in result]
            keyboard = types.InlineKeyboardMarkup(row_width=4)
            keyboard.add(*buttons)
            await call.message.edit_text(f"Выберите {call.data}", reply_markup=keyboard)

    executor.start_polling(dp, skip_updates=True)
