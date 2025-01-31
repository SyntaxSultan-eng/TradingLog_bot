from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Данные сделок📋"), KeyboardButton(text ="Модицикация🔨")],
    [KeyboardButton(text="Полная статистика📊")],
    [KeyboardButton(text="Новая запись📝")]
],
    resize_keyboard=True,
    input_field_placeholder="Выберите режим",
)

new_deal_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Покупка📈"), KeyboardButton(text="Продажа📉")]
],
    resize_keyboard=True,
    input_field_placeholder="Какой тип у сделки?",
)