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
    [KeyboardButton(text="Покупка📈"), KeyboardButton(text="Продажа📉")],
    [KeyboardButton(text="Назад🔙")]
],
    resize_keyboard=True,
    input_field_placeholder="Какой тип у сделки?",
    one_time_keyboard=True,
)

full_statistic_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Полная статистика📋", callback_data="full_static")],
    [InlineKeyboardButton(text="Прибыль по акциям📈", callback_data="profit-stocks")],
    [InlineKeyboardButton(text="Графики📊", callback_data="graph")]
])

names_stocks_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Вывести", callback_data="print_info")],
    [InlineKeyboardButton(text = "Не нужно", callback_data="no_print_info")] 
])