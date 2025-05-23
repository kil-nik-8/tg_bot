from typing import List

from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from lexicon import buttons, callbacks


class UserKeyboards:
    @staticmethod
    def start() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=buttons["begin_work"])],
                [KeyboardButton(text=buttons["help"])],
            ],
            resize_keyboard=True,
        )

        return kb


    @staticmethod
    def cancel_registration_reply_kb() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=buttons["cancel_registration"])]
            ],
            resize_keyboard=True,
        )

        return kb

    @staticmethod
    def confirm_cancel_kb():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm"),
                    InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
                    ]
            ]
        )
    
    @staticmethod
    def cancel_read_sheet_kb():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
            ]
        )
    
    @staticmethod
    def build_options_keyboard(selected: list) -> InlineKeyboardMarkup:
        OPTIONS = ["Вариант 1", "Вариант 2", "Вариант 3"]
        keyboard = []
        for idx, option in enumerate(OPTIONS):
            prefix = "✅ " if idx in selected else ""
            keyboard.append([
                InlineKeyboardButton(
                    text=prefix + option,
                    callback_data=f"option_{idx}"
                )
            ])
        # Кнопка "Готово"
        keyboard.append([InlineKeyboardButton(text="Готово", callback_data="done")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @staticmethod
    def cancel_registration() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(
                text=buttons["cancel_registration"],
                callback_data=callbacks[buttons["cancel_registration"]],
            )
        )

        return kb.as_markup()

    @staticmethod
    def confirm_cancelling() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(
                text=buttons['YES'],
                callback_data=callbacks[buttons['YES']],
            ),
            InlineKeyboardButton(
                text=buttons['NO'],
                callback_data=callbacks[buttons['NO']],
            )
        ).adjust(1)

        return kb.as_markup()


    @staticmethod
    def request_phone_number() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Отправить", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

        return kb
