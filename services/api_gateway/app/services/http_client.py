from curl_cffi.requests import AsyncSession


async def http_get(url, **kwargs):
    async with AsyncSession(
        impersonate='chrome123'
    ) as session:
        r = await session.get(url, **kwargs)
        r.raise_for_status()
        return r.json()


async def http_post(url, json=None, **kwargs):
    async with AsyncSession(
        impersonate='chrome123'
    ) as session:
        r = await session.post(url, json=json, **kwargs)
        r.raise_for_status()
        return r.json()


async def http_delete(url, **kwargs):
    async with AsyncSession(
        impersonate='chrome123'
    ) as session:
        r = await session.delete(url, **kwargs)
        r.raise_for_status()
        return r.json() if r.content else None
