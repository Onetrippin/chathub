from telegram import Update
from telegram.ext import ContextTypes

from database.connection import SessionLocal
from bot.keyboards import inline_main_menu
from database.repositories.users import get_user_by_tg
from database.repositories.settings import get_settings, toggle_theme, toggle_notifications
from database.repositories.integrations import list_integrations
from database.repositories.notifications import last_notifications
from database.repositories.files import list_files


def _fmt_dt(dt) -> str:
    return dt.strftime("%Y-%m-%d %H:%M") if dt else "—"


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_hide":
        await query.edit_message_text("Меню закрыто. Напиши /menu чтобы открыть снова.")
        return

    tg = update.effective_user
    async with SessionLocal() as session:
        user = await get_user_by_tg(session, tg.id)
        if not user:
            await query.edit_message_text("Профиль не найден. Нажми /start.", reply_markup=inline_main_menu())
            return

        if data == "profile":
            text = (
                "Профиль\n"
                f"• Имя: {user.first_name or '—'} {user.last_name or ''}\n"
                f"• Username: @{user.username}" if user.username else "• Username: —"
            )
            text += (
                f"\n• Telegram ID: {user.telegram_id}\n"
                f"• User ID: {user.id}\n"
                f"• Создан: {_fmt_dt(user.created_at)}\n"
                f"• Последняя активность: {_fmt_dt(user.last_seen_at)}"
            )
            await query.edit_message_text(text, reply_markup=inline_main_menu())
            return

        if data == "settings":
            s = await get_settings(session, user.id)
            text = (
                "Настройки\n"
                f"• Тема: {s.theme}\n"
                f"• Язык: {s.language}\n"
                f"• Таймзона: {s.timezone}\n"
                f"• AI-персона: {s.ai_persona}\n"
                f"• Уведомления: {'включены' if s.notifications_enabled else 'выключены'}\n\n"
                "Действия:\n"
                "• /menu → «Настройки» (inline) и нажми снова после переключения\n\n"
                "Команды переключения:\n"
                "• (кнопками сделаем позже) сейчас через callback: settings_toggle_theme / settings_toggle_notif"
            )
            await query.edit_message_text(text, reply_markup=inline_main_menu())
            return

        # “скрытые” callback’и для переключения (их можно добавить кнопками позже)
        if data == "settings_toggle_theme":
            s = await toggle_theme(session, user.id)
            await query.edit_message_text(f"Тема переключена на: {s.theme}", reply_markup=inline_main_menu())
            return

        if data == "settings_toggle_notif":
            s = await toggle_notifications(session, user.id)
            await query.edit_message_text(
                f"Уведомления теперь: {'включены' if s.notifications_enabled else 'выключены'}",
                reply_markup=inline_main_menu(),
            )
            return

        if data == "integrations":
            items = await list_integrations(session, user.id)
            if not items:
                await query.edit_message_text("Интеграций нет. Выполни /seed.", reply_markup=inline_main_menu())
                return
            lines = ["Интеграции:"]
            for it in items:
                lines.append(f"• {it.platform}: {it.status} (last_sync: {_fmt_dt(it.last_sync_at)})")
            await query.edit_message_text("\n".join(lines), reply_markup=inline_main_menu())
            return

        if data == "notifications":
            items = await last_notifications(session, user.id, limit=7)
            if not items:
                await query.edit_message_text("Уведомлений нет. Выполни /seed.", reply_markup=inline_main_menu())
                return
            lines = ["Последние уведомления:"]
            for n in items:
                lines.append(f"• {_fmt_dt(n.created_at)} — {n.type}: {n.payload}")
            await query.edit_message_text("\n".join(lines), reply_markup=inline_main_menu())
            return

        if data == "files":
            items = await list_files(session, user.id, limit=10)
            if not items:
                await query.edit_message_text("Файлов нет. Выполни /seed.", reply_markup=inline_main_menu())
                return
            lines = ["Файлы:"]
            for f in items:
                lines.append(f"• {f.filename} — {f.size_bytes} bytes — {f.file_type} — {_fmt_dt(f.created_at)}")
            await query.edit_message_text("\n".join(lines), reply_markup=inline_main_menu())
            return

        if data == "ai_demo":
            await query.edit_message_text(
                "AI-демо работает через текстовый режим:\n"
                "Нажми в Reply-меню «AI: спросить ассистента» и отправь запрос.\n"
                "История будет сохраняться в БД.",
                reply_markup=inline_main_menu(),
            )
            return

    await query.edit_message_text(f"Неизвестная кнопка: {data}", reply_markup=inline_main_menu())
