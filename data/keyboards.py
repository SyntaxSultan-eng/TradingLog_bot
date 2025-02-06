from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

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
    one_time_keyboard=True,
)

names_stocks_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Вывести", callback_data="print_info")],
    [InlineKeyboardButton(text = "Не нужно", callback_data="no_print_info")] 
])