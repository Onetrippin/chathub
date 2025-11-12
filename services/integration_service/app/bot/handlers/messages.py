from telegram import Update
from telegram.ext import ContextTypes

from database.connection import SessionLocal
from bot.keyboards import reply_main_menu
from bot.handlers.commands import help_cmd
from database.repositories.users import get_user_by_tg
from database.repositories.ai import add_ai_history


def _fake_ai(prompt: str) -> str:
    return (
        "План действий:\n"
        "1) Поднять API Gateway и эндпоинт /auth/telegram.\n"
        "2) Message Service: WebSocket + Redis Pub/Sub.\n"
        "3) Storage: MinIO + presigned upload/download.\n"
        "4) AI: очередь задач + история.\n"
        "5) Набор тестов: smoke API + WebSocket сценарии.\n\n"
        f"Следующий шаг: уточнить требования к экрану Mini App для «{prompt[:60]}»."
    )


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt_raw = update.message.text or ""
    txt = txt_raw.strip().lower()

    if txt == "помощь":
        await help_cmd(update, context)
        return

    tg = update.effective_user
    async with SessionLocal() as session:
        user = await get_user_by_tg(session, tg.id)

    if txt == "профиль":
        if not user:
            await update.message.reply_text("Профиль не найден. Нажми /start.", reply_markup=reply_main_menu())
            return
        await update.message.reply_text(
            f"Профиль\n"
            f"• Имя: {user.first_name or '—'} {user.last_name or ''}\n"
            f"• Username: @{user.username}" if user.username else f"Профиль\n• Имя: {user.first_name or '—'} {user.last_name or ''}\n• Username: —",
            reply_markup=reply_main_menu(),
        )
        return

    if txt == "настройки":
        await update.message.reply_text(
            "Открой /menu → «Настройки» (там информация из БД).",
            reply_markup=reply_main_menu(),
        )
        return

    if txt in ("ai: спросить ассистента", "ai"):
        if not user:
            await update.message.reply_text("Сначала /start", reply_markup=reply_main_menu())
            return
        context.user_data["awaiting_ai_prompt"] = True
        await update.message.reply_text("Напиши запрос для ассистента:", reply_markup=reply_main_menu())
        return

    if context.user_data.get("awaiting_ai_prompt"):
        context.user_data["awaiting_ai_prompt"] = False
        if not user:
            await update.message.reply_text("Сначала /start", reply_markup=reply_main_menu())
            return

        prompt = txt_raw.strip()
        response = _fake_ai(prompt)

        async with SessionLocal() as session:
            db_user = await get_user_by_tg(session, tg.id)
            if db_user:
                await add_ai_history(session, db_user.id, prompt=prompt, response=response, tokens_used=220)

        await update.message.reply_text(
            f"AI-ассистент\nЗапрос: {prompt}\n\nОтвет:\n{response}",
            reply_markup=reply_main_menu(),
        )
        return

    if txt == "интеграции":
        await update.message.reply_text("Открой /menu → «Интеграции» (данные из БД).", reply_markup=reply_main_menu())
        return

    if txt == "уведомления":
        await update.message.reply_text("Открой /menu → «Уведомления» (данные из БД).", reply_markup=reply_main_menu())
        return

    if txt == "файлы":
        await update.message.reply_text("Открой /menu → «Файлы» (данные из БД).", reply_markup=reply_main_menu())
        return

    await update.message.reply_text("Жми кнопки меню или открой Mini App.", reply_markup=reply_main_menu())
