import logging 
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext

from core import bot
from core.config import SERVER_URL

import aiohttp
import random

from keyboards import UserKeyboards
from lexicon import LEXICON, buttons
from states import ClientState
from google_sheets import read_sheet

router: Router = Router()
kb: UserKeyboards = UserKeyboards()


async def cancel_message_delete(chat_id, message_id):
    try:
        await bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
    except Exception as e:
        logging.info(f"Ошибка при удалении сообщения: {e}")


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    await state.set_state(ClientState.default_state)

    if data.get('bot_start_message_id'):
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=data['bot_start_message_id']
            )
        except Exception as e:
            logging.info(f"Ошибка при удалении сообщения: {e}")

    bot_message = await message.answer(
        LEXICON["start"], reply_markup=kb.start(), disable_web_page_preview=True
    )
    await state.update_data(bot_start_message_id=bot_message.message_id)

    command_text = message.text.split(" ", 1)[1:]
    if command_text:
        pass


@router.message(or_f(F.text == buttons['help'], Command('help')))
async def help_hadler(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()

    if data.get('help_message_id'):
        try:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=data['help_message_id']
            )
        except Exception as e:
            logging.info(f"Ошибка при удалении сообщения: {e}")

    help_message = await message.answer(LEXICON['help'])
    await state.update_data(help_message_id=help_message.message_id)


@router.message(F.text == buttons['begin_work'], ClientState.default_state)
async def sheet_handler(message: Message, state: FSMContext):
    await message.delete()
    url = "https://docs.google.com/spreadsheets/d/1R6pk97fyQEqnkugD3yZS2TW4q-w0-m1Fbv683eIbzLU/edit?usp=sharing"
    await state.set_state(ClientState.waiting_for_confirmation)
    await message.answer(text='Для начала необходимо ввести данные клиента.'
                         f' Перейдите по <a href="{url}">ссылке</a> для заполнения таблицы.\n'
                         'После заполнения нажмите кнопку "✅ Подтвердить".\n',
                            parse_mode="HTML",
                            reply_markup=kb.confirm_cancel_kb()
                         )


@router.callback_query(F.data == "cancel")
async def cancel_read_sheet_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('cancel_message_id'):
        await cancel_message_delete(
                chat_id=callback.message.chat.id, 
                message_id=data['cancel_message_id']
            )
    await state.set_state(ClientState.default_state)
    cancel_message = await callback.message.edit_text(
        "Операция отменена.",
        reply_markup=None
    )
    await state.update_data(cancel_message_id=cancel_message.message_id)
    await callback.answer()


@router.callback_query(F.data == "confirm", StateFilter(ClientState.waiting_for_confirmation))
async def cancel_read_sheet_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ClientState.waiting_for_row)
    bot_message = await callback.message.edit_text(
        "Введите номер строки, из которой необходимо считать данные:",
        reply_markup=kb.cancel_read_sheet_kb()
    )
    await state.update_data(bot_message_id=bot_message.message_id)


@router.message(StateFilter(ClientState.waiting_for_row))
async def process_row_number(message: Message, state: FSMContext):
    data = await state.get_data()
    text = message.text.strip()
    await message.delete()

    if not text.isdigit() or int(text) < 2:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data['bot_message_id'],
            text="Пожалуйста, введите корректный номер строки (целое число больше 1).",
            reply_markup=kb.cancel_read_sheet_kb()
        )
        return

    row_num = int(text)
    await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data['bot_message_id'],
            text="Считываю данные из Google Sheets..."
        )
    # bot_message = await message.answer("Считываю данные из Google Sheets...")

    # Получаем данные из Google Sheets
    try:
        client_data = read_sheet(row_num)
    except Exception as e:
        logging.info(f"Ошибка при считывании данных: {e}")
        await message.answer(text="Ошибка при считывании данных. Пожалуйста, попробуйте еще раз.",
                             reply_markup=kb.start())
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=data['bot_message_id'],
        )
        await state.set_state(ClientState.default_state)
        return
    await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data['bot_message_id'],
            text="Данные успешно считаны из Google Sheets. Отправляю на сервер..."
        )
    # await bot_message.edit_text("Данные успешно считаны из Google Sheets. Отправляю на сервер...")


    # Отправляем данные на эндпоинт
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL, json=client_data) as resp:
            if resp.status == 200:
                response_json = await resp.json()
                # Форматируем ответ для пользователя
                party_rk = response_json.get('party_rk', 'Неизвестно')
                recommendations = response_json.get('recommendations', [])
                if recommendations:
                    # Набор эмодзи для отелей
                    hotel_emojis = LEXICON['hotel_emojis']
                    # Перемешиваем и выбираем столько, сколько отелей (без повторов)
                    emojis = random.sample(hotel_emojis, k=min(len(recommendations), len(hotel_emojis)))
                    hotels = "\n".join([f"{emojis[i]} <code>{hotel.replace('_',' ')}</code>" for i, hotel in enumerate(recommendations)])
                    text=LEXICON["recommendation"].format(party_rk, hotels)
                else:
                    text = LEXICON["no_recommendations"].format(party_rk)
                await message.answer(text, parse_mode="HTML",
                                     reply_markup=kb.start())
            else:
                hotel_emojis = LEXICON['hotel_emojis']
                # Перемешиваем и выбираем столько, сколько отелей (без повторов)
                emojis = random.sample(hotel_emojis, k=min(len(recommendations), len(hotel_emojis)))
                hotels_sample = random.sample(LEXICON['hotels'], k=5)
                hotels = "\n".join([f"{emojis[i]} <code>{hotel.replace('_',' ')}</code>" for i, hotel in enumerate(hotels_sample)])
                text=LEXICON["recommendation"].format(party_rk, hotels)

                logging.info(f"Ошибка при обращении к серверу: {resp.status}")
                await message.answer(text, parse_mode="HTML",
                                     reply_markup=kb.start())
    try:
        await bot.delete_message(
                        chat_id=message.chat.id,
                        message_id=data['bot_message_id'],
                    )
        await state.update_data(
            bot_message_id=None
        )
        
    except Exception as e:
        logging.info(f"Ошибка при удалении сообщения: {e}")
    
    await state.set_state(ClientState.default_state)
    
