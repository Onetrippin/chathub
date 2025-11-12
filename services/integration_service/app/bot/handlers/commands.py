from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.config import MINI_APP_URL
from database.connection import SessionLocal
from bot.keyboards import reply_main_menu, inline_main_menu
from database.repositories.users import upsert_user, delete_user_by_tg, get_user_by_tg
from database.repositories.integrations import seed_integrations
from database.repositories.notifications import seed_notifications
from database.repositories.files import seed_files


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg = update.effective_user
    async with SessionLocal() as session:
        user = await upsert_user(
            session=session,
            telegram_id=tg.id,
            username=tg.username,
            first_name=tg.first_name,
            last_name=tg.last_name,
        )

    text = (
        f"Привет, {tg.first_name or 'друг'}!\n\n"
        f"Профиль создан/обновлён в БД.\n"
        f"Внутренний user_id: {user.id}\n\n"
        "Жми кнопки меню или открывай Mini App."
    )
    await update.message.reply_text(text, reply_markup=reply_main_menu(), parse_mode=ParseMode.HTML)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Меню:", reply_markup=inline_main_menu())


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Команды:\n"
        "/start — регистрация/обновление профиля\n"
        "/menu — меню под сообщением\n"
        "/miniapp — вход в Mini App\n"
        "/seed — создать данные в БД (интеграции/уведомления/файлы)\n"
        "/resetme — удалить все данные пользователя из БД\n"
        "/hide — убрать клавиатуру",
        reply_markup=reply_main_menu(),
    )


async def miniapp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kb = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Открыть Mini App", web_app=WebAppInfo(url=MINI_APP_URL))]]
    )
    await update.message.reply_text("Вход в Mini App:", reply_markup=kb)


async def hide(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Клавиатура скрыта.", reply_markup=ReplyKeyboardRemove())


async def seed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg = update.effective_user
    async with SessionLocal() as session:
        user = await get_user_by_tg(session, tg.id)
        if not user:
            await update.message.reply_text("Сначала /start", reply_markup=reply_main_menu())
            return
        await seed_integrations(session, user.id)
        await seed_notifications(session, user.id)
        await seed_files(session, user.id)

    await update.message.reply_text(
        "Данные записаны в БД: интеграции, уведомления, файлы.",
        reply_markup=reply_main_menu(),
    )


async def resetme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg = update.effective_user
    async with SessionLocal() as session:
        await delete_user_by_tg(session, tg.id)

    await update.message.reply_text(
        "Данные пользователя удалены из БД. Напиши /start чтобы создать заново.",
        reply_markup=reply_main_menu(),
    )
