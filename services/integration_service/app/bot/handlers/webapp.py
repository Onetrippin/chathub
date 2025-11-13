from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.keyboards import reply_main_menu


async def on_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    wad = update.message.web_app_data
    data = wad.data if wad else ""
    await update.message.reply_text(
        f"Получены данные из Mini App:\n<code>{data}</code>\n\n"
        "Позже: распарсим payload и отправим в нужный сервис.",
        parse_mode=ParseMode.HTML,
        reply_markup=reply_main_menu(),
    )
