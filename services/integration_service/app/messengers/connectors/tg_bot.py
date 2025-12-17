from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from messengers.models import InboundMessageEvent
from messengers.publisher import MessagePublisher


class TelegramBotConnector:
    def __init__(self, bot_token: str, internal_user_id: str, publisher: MessagePublisher):
        self.bot_token = bot_token
        self.internal_user_id = internal_user_id
        self.publisher = publisher
        self.app = Application.builder().token(self.bot_token).build()

        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_text))
        self.app.add_handler(MessageHandler(filters.CaptionRegex(r".*"), self.on_caption))

    async def on_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        msg = update.effective_message
        chat = update.effective_chat
        user = update.effective_user

        ev = InboundMessageEvent(
            platform="telegram_bot",
            user_id=self.internal_user_id,
            external_chat_id=str(chat.id),
            external_message_id=str(msg.message_id),
            sender_external_id=str(user.id) if user else "",
            text=msg.text or "",
            timestamp=datetime.utcnow(),
            raw={"chat_type": chat.type, "username": getattr(user, "username", None)},
        )
        await self.publisher.publish_inbound(ev)

    async def on_caption(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        msg = update.effective_message
        chat = update.effective_chat
        user = update.effective_user

        ev = InboundMessageEvent(
            platform="telegram_bot",
            user_id=self.internal_user_id,
            external_chat_id=str(chat.id),
            external_message_id=str(msg.message_id),
            sender_external_id=str(user.id) if user else "",
            text=(msg.caption or ""),
            timestamp=datetime.utcnow(),
            raw={"has_media": True, "chat_type": chat.type},
        )
        await self.publisher.publish_inbound(ev)

    async def run_polling(self) -> None:
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        await self.app.updater.wait()
