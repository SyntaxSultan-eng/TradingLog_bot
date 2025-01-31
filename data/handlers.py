from decouple import config
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext

import data.keyboards as keyboard
import data.requests as rq

######################################

router = Router()

class Stocks(StatesGroup):
    name_stock = State()
    amount = State()
    trade_date = State()
    price = State()
    type_of_stock = State()
    info = State()

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


@router.message(F.text == "Покупка📈")
async def buy_deal(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id == int(config("Admin_ID")):
        await message.answer(
            "Введите <b>название акции</b>, которую Вы купили.",
            parse_mode = "HTML",
        )
        await state.set_state(Stocks.name_stock) 
        return
    await message.answer(
        "<i>Извините, но это частный бот.</i>",
        parse_mode="HTML",
    )

@router.message(Stocks.name_stock)
async def name_of_stock(message: types.Message, state: FSMContext):
    await state.update_data(name_stock = message.text)
    data = await state.get_data()
    await rq.add_name_stock(data['name_stock'])
    
    await message.answer(
        "SPS",
        reply_markup=keyboard.main_keyboard,
    )
    await state.clear()


#######################################