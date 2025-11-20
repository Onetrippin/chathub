import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.config import BOT_TOKEN
from database.connection import init_db
from bot.handlers.commands import start, menu, help_cmd, miniapp, hide, seed, resetme
from bot.handlers.callbacks import on_callback
from bot.handlers.messages import on_text
from bot.handlers.webapp import on_web_app_data


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN (переменная окружения).")

    asyncio.run(init_db())

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("miniapp", miniapp))
    app.add_handler(CommandHandler("hide", hide))

    app.add_handler(CommandHandler("seed", seed))
    app.add_handler(CommandHandler("resetme", resetme))

    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, on_web_app_data))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
