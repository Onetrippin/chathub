from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from messengers.models import InboundMessageEvent
from messengers.publisher import MessagePublisher


class TelegramUserbotConnector:
    def __init__(
        self,
        api_id: int,
        api_hash: str,
        session_string: str,
        internal_user_id: str,
        publisher: MessagePublisher,
    ):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_string = session_string
        self.internal_user_id = internal_user_id
        self.publisher = publisher

        self.client = TelegramClient(StringSession(self.session_string), self.api_id, self.api_hash)

    async def start(self) -> None:
        await self.client.start()

        @self.client.on(events.NewMessage)
        async def handler(event):
            msg = event.message
            chat = await event.get_chat()
            sender = await event.get_sender()

            external_chat_id = str(getattr(chat, "id", msg.peer_id))
            external_msg_id = str(msg.id)
            sender_id = str(getattr(sender, "id", ""))

            ev = InboundMessageEvent(
                platform="telegram_user",
                user_id=self.internal_user_id,
                external_chat_id=external_chat_id,
                external_message_id=external_msg_id,
                sender_external_id=sender_id,
                text=msg.message or "",
                timestamp=datetime.utcnow(),
                raw={"chat": str(chat), "sender": str(sender)},
            )
            await self.publisher.publish_inbound(ev)

    async def run(self) -> None:
        await self.start()
        await self.client.run_until_disconnected()

    async def list_dialogs(self, limit: int = 20):
        dialogs = []
        async for d in self.client.iter_dialogs(limit=limit):
            dialogs.append({"id": d.id, "name": d.name, "unread": d.unread_count})
        return dialogs

    async def send_message(self, peer_id: str, text: str) -> None:
        await self.client.send_message(entity=int(peer_id), message=text)
