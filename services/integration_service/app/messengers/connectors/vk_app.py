import asyncio
from datetime import datetime

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from messengers.models import InboundMessageEvent
from messengers.publisher import MessagePublisher


class VKAppConnector:
    def __init__(
        self,
        vk_token: str,
        internal_user_id: str,
        publisher: MessagePublisher,
        poll_interval_sec: float = 0.0,
    ):
        self.vk_token = vk_token
        self.internal_user_id = internal_user_id
        self.publisher = publisher
        self.poll_interval_sec = poll_interval_sec

        self.vk_session = vk_api.VkApi(token=self.vk_token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)

    def send_message(self, peer_id: int, text: str) -> None:
        self.vk.messages.send(peer_id=peer_id, message=text, random_id=0)

    async def run(self) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._listen_blocking)

    def _listen_blocking(self) -> None:
        for event in self.longpoll.listen():
            if event.type != VkEventType.MESSAGE_NEW:
                continue

            text = event.text or ""
            peer_id = str(getattr(event, "peer_id", ""))
            msg_id = str(getattr(event, "message_id", "")) or f"vk:{datetime.utcnow().timestamp()}"

            ev = InboundMessageEvent(
                platform="vk",
                user_id=self.internal_user_id,
                external_chat_id=peer_id,
                external_message_id=msg_id,
                sender_external_id=str(getattr(event, "user_id", "")),
                text=text,
                timestamp=datetime.utcnow(),
                raw={"peer_id": getattr(event, "peer_id", None), "text": text},
            )

            asyncio.run(self.publisher.publish_inbound(ev))
