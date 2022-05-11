# import telebot
# from telebot import *
from datetime import datetime
from aiogram import *
from bd import *

back = '⬅ Назад'
lunch = 12 * 60 + 25
lessons = ((495, 545, 600, 655, 705, 12 * 60 + 35, 13 * 60 + 50,
            14 * 60 + 35, 15 * 60 + 20, 16 * 60 + 40, 17 * 60 + 20),
           (535, 585, 640, 695, 12 * 60 + 24, 13 * 60 + 44,
            14 * 60 + 30, 15 * 60 + 15, 16 * 60, 17 * 60 + 19, 18 * 60))


def botik(token):
    bot = Bot(token)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start', 'help'])
    async def keyboard(message: types.Message):
        result = request(f"SELECT * FROM bot_db.main;")
        buttons = [types.InlineKeyboardButton(text=row[0], callback_data=row[1]) for row in result]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await bot.send_message(message.from_user.id, "Добро пожаловать", reply_markup=keyboard)

    @dp.callback_query_handler()
    async def callback(call: types.CallbackQuery):
        if call.data == 'tc':
            result = request(f"SELECT * FROM bot_db.d{datetime.now().weekday() + 1};")
            buttons = [types.InlineKeyboardButton(text=row[0], callback_data=row[0]) for row in result]
            keyboard = types.InlineKeyboardMarkup(row_width=4)
            keyboard.add(*buttons)
            await call.message.edit_text(f"Выберите учителя", reply_markup=keyboard)
        elif call.data != 'tc' and call.data != 'classes' and call.data != 'main':
            buttons = [types.InlineKeyboardButton(back)]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            result = request(f"SELECT * FROM bot_db.{datetime.now().weekday() + 1} WHERE buttons = {call.data};")
            weekday = datetime.now().weekday() + 1
            time = int(datetime.now().time().hour) * 60 + int(datetime.now().time().minute)
            x = 0
            for i in lessons[1]:
                x = lessons[1].index(i)
                if time <= i:
                    break
            if lunch < time < lunch + 50:
                await call.message.edit_text(f"Cкорее всего в Столовой, Учительской, {result[x + 2]}, {result[x + 3]}",
                                             reply_markup=keyboard)  # ЩА ОБЕД
            else:
                await call.message.edit_text(f"Cкорее всего в Учительской, {result[x + 2]}, {result[x + 3]}",
                                             reply_markup=keyboard)  # КАК ОБЫЧНО
        else:
            result = request(f"SELECT * FROM bot_db.{call.data};")
            buttons = [types.InlineKeyboardButton(text=row[0], callback_data=row[1]) for row in result]
            keyboard = types.InlineKeyboardMarkup(row_width=4)
            keyboard.add(*buttons)
            await call.message.edit_text(f"Выберите {call.data}", reply_markup=keyboard)

    executor.start_polling(dp, skip_updates=True)
