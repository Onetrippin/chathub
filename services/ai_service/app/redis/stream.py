import json
import aioredis

REDIS_URL = 'redis://redis:6379'
STREAM_NAME = 'ai:tasks'


async def push_task(user_id: str, prompt: str, model: str = 'gpt-5'):
    redis = await aioredis.from_url(REDIS_URL)
    data = {'user_id': user_id, 'prompt': prompt, 'model': model}
    await redis.xadd(STREAM_NAME, {'data': json.dumps(data)})
    await redis.close()


async def consume_tasks(group_name='ai_group', consumer_name='ai_worker'):
    redis = await aioredis.from_url(REDIS_URL)
    await redis.xgroup_create(name=STREAM_NAME, groupname=group_name, id='$', mkstream=True)
    while True:
        msgs = await redis.xreadgroup(group_name, consumer_name, streams={STREAM_NAME: '>'}, count=1, block=5000)
        if not msgs:
            continue
        for stream, messages in msgs:
            for msg_id, fields in messages:
                data = json.loads(fields[b'data'].decode())
                # Здесь будет логика генерации ответа модели
                print(f'AI task received: {data}')
                await redis.xack(STREAM_NAME, group_name, msg_id)
