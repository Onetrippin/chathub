from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

from bot.config import MINI_APP_URL


def reply_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [KeyboardButton(text="Профиль"), KeyboardButton(text="Настройки"), KeyboardButton(text="Помощь")],
        [KeyboardButton(text="Интеграции"), KeyboardButton(text="Уведомления")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def inline_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))],
        [
            InlineKeyboardButton("Профиль", callback_data="profile"),
            InlineKeyboardButton("Настройки", callback_data="settings"),
        ],
        [
            InlineKeyboardButton("Интеграции", callback_data="integrations"),
            InlineKeyboardButton("Уведомления", callback_data="notifications"),
        ],
        [InlineKeyboardButton("Закрыть меню", callback_data="menu_hide")],
    ]
    return InlineKeyboardMarkup(keyboard)
