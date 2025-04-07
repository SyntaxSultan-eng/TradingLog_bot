from decouple import config
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

import data.keyboards as keyboard
import data.request as rq
import os


######################################

router = Router()

class Stocks(StatesGroup):
    name_stock = State()
    amount = State()
    price = State()
    deal_type = State()

######################################

############# Команды ################

@router.message(Command('start'))
async def start_check(message: types.Message) -> None:
    if message.from_user.id == int(config("Admin_ID")):
        await message.answer(
            "<i>Здравствуйте, Влад</i>! Начните же инвестировать.",
            reply_markup=keyboard.main_keyboard,
            parse_mode="HTML"
        )
        return
    
    await message.answer(
        "<i>Извините, но это частный бот.</i>",
        parse_mode="HTML"
    )

#######################################

############ Новая запись📝 ##########

@router.message(F.text == "Новая запись📝")
async def new_deal(message: types.Message) -> None:
    if message.from_user.id == int(config("Admin_ID")):
        await message.answer(
            "Подготавливаем для Вашей сделки место в Базе данных.⚙️",
        )
        await message.answer(
            "<i>Выберите тип сделки.</i>",
            parse_mode = "HTML",
            reply_markup=keyboard.new_deal_keyboard,
        )
        return
    await message.answer(
        "<i>Извините, но это частный бот.</i>",
        parse_mode="HTML"
    )

@router.message(F.text == "Назад🔙")
async def return_back(message: types.Message, state: FSMContext):
    if message.from_user.id == int(config("Admin_ID")):
        await message.answer(
            "Возвращаю Вас на главное меню!🔙",
            reply_markup=keyboard.main_keyboard
        )
        await state.clear()
        return
    await message.answer(
        "<i>Извините, но это частный бот.</i>",
        parse_mode="HTML"
    )

@router.message(F.text == "Покупка📈")
async def buy_deal(message: types.Message, state: FSMContext):
    if message.from_user.id == int(config("Admin_ID")):
        await message.answer(
            "Введите <b>название акции</b>, которую Вы купили.",
            parse_mode="HTML"
        )
        await message.answer(
            "<u><b>ВАЖНО!</b></u>\n\nМожно указать и тикер акции, но обязательно необходимо написать <b>существующую</b> ценную бумагу.(пока только Ru рынок акций)\n\n" + \
            "Вы можете вывести все доступные акции и их тикеры.",
            parse_mode = "HTML",
            reply_markup=keyboard.names_stocks_inline
        )
        await state.update_data(deal_type = "Покупка")
        return
    await message.answer(
        "<i>Извините, но это частный бот.</i>",
        parse_mode="HTML",
    )

@router.message(F.text == "Продажа📉")
async def sell_deal(message: types.Message, state:FSMContext):
    if message.from_user.id == int(config("Admin_ID")):
        await message.answer(
            "Введите <b>название акции</b>, которую Вы продали.",
            parse_mode="HTML"
        )
        await message.answer(
            "<u><b>ВАЖНО!</b></u>\n\nМожно указать и тикер акции, но обязательно необходимо написать <b>существующую</b> ценную бумагу.(пока только Ru рынок акций)\n\n" + \
            "Вы можете вывести все доступные акции и их тикеры.",
            parse_mode = "HTML",
            reply_markup=keyboard.names_stocks_inline
        )
        await state.update_data(deal_type = "Продажа")
        return
    await message.answer(
        "<i>Извините, но это частный бот.</i>",
        parse_mode="HTML",
    )

@router.callback_query(F.data == "print_info")
async def print_stocks_names(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    file_path = os.path.join("data","requirements","Акции.pdf")
    json_file = types.FSInputFile(file_path)

    await callback.message.answer_document(
        document=json_file,
        caption="Тикеры и названия акций."
    )
    
    await callback.message.answer(
        "Вы можете продолжить ввод названия.↓"
    )
    await state.set_state(Stocks.name_stock)

@router.callback_query(F.data == "no_print_info")
async def no_print(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(Stocks.name_stock)    

@router.message(Stocks.name_stock)
async def name_of_stock(message: types.Message, state: FSMContext):
    await state.update_data(name_stock = message.text)
    data = await state.get_data()
    check = await rq.check_names(data['name_stock'])
    
    if not check:
        await state.clear()
        await message.answer(
            "<i>Нет такой ценной бумаги!</i>",
            parse_mode="HTML",
            reply_markup=keyboard.main_keyboard
        )
        return
    await state.set_state(Stocks.amount)
    await message.answer(
        "Введите <i><b>количество</b></i> акций, которое участвовало в сделке.<i><b>(разрешены только натуральные числа)</b></i>",
        parse_mode="HTML"
    )

@router.message(Stocks.amount)
async def amount_of_stock(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or message.text == '0':
        await message.answer(
            "<i><b>Разрешены только натуральные числа!</b></i>",
            parse_mode="HTML",
            reply_markup=keyboard.main_keyboard
        )
        await state.clear()
        return
    await state.update_data(amount = int(message.text))
    await message.answer(
        "Введите <b><i>полную цену</i></b> сделки.(без комиссии брокера)\n\n<b><i>Только рациональные числа >0(для десятичных дробей использовать .)</i></b>",
        parse_mode="HTML"
    )
    await state.set_state(Stocks.price)

@router.message(Stocks.price)
async def price_of_stock(message: types.Message, state: FSMContext):
    try:
        price_stock = float(message.text)
        if price_stock > 0:
            await state.update_data(price = price_stock)
            await message.answer(
                "Заносим данные в Базу данных.⚙️",
            )

            data = await state.get_data()
            await rq.add_new_stock(data['name_stock'],data['amount'],data['price'],data['deal_type'])

            await message.answer(
                "<i><b>Данные были успешно добавлены.</b></i>",
                reply_markup=keyboard.main_keyboard,
                parse_mode="HTML"
            )
        else:
           await message.answer(
                "<i><b>Только рациональные числа >0</b></i>",
                parse_mode="HTML",
                reply_markup=keyboard.main_keyboard
            )
        await state.clear()
        return 
    except ValueError:
        await message.answer(
            "<i><b>Только рациональные числа >0</b></i>",
            parse_mode="HTML",
            reply_markup=keyboard.main_keyboard
        )
        await state.clear()        

#######################################

######### Полная статистика📊 ######

@router.message(F.text == "Полная статистика📊")
async def full_statistic(message: types.Message):
    if message.from_user.id != int(config("Admin_ID")):
        await message.answer(
            "<i>Извините, но это частный бот.</i>",
            parse_mode="HTML"
        )
        return
    
    await message.answer(
        "<i>Выберите режим</i>.⤵️",
        parse_mode="HTML",
        reply_markup=keyboard.full_statistic_buttons
    )

@router.callback_query(F.data == "full_static")
async def handle_full_stats(callback: types.CallbackQuery):
    await callback.message.delete()

    info = await rq.full_info()

    await callback.message.answer(
        "🔁 <b>Сделки:</b>\n"
        f"• Всего: {info['total_deals']} ({info["total_deals_buy"]} покупок / {info["total_deals_sell"]} продаж)\n"
        f"• Полная сумма покупок: {info["total_buy"]} ₽\n"
        f"• Полная сумма продаж: {info["total_sell"]} ₽\n",
        parse_mode= "HTML",
        reply_markup=keyboard.main_keyboard
    )

@router.callback_query(F.data == "profit-stocks")
async def handler_profit(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "В разработке",
        reply_markup=keyboard.main_keyboard
    )

@router.callback_query(F.data == "graph")
async def handler_graph(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "В разработке",
        reply_markup=keyboard.main_keyboard
    )