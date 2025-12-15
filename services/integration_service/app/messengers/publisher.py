from curl_cffi.requests import AsyncSession
from messengers.models import InboundMessageEvent


class MessagePublisher:
    def __init__(self, message_service_url: str, impersonate: str = "chrome123"):
        self.message_service_url = message_service_url.rstrip("/")
        self.impersonate = impersonate

    async def publish_inbound(self, event: InboundMessageEvent) -> None:
        url = f"{self.message_service_url}/integrations/inbound"
        async with AsyncSession(impersonate=self.impersonate) as s:
            r = await s.post(url, json=event.model_dump())
            r.raise_for_status()
