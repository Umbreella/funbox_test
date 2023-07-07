import asyncio
from contextlib import ExitStack

import pytest
import redis
from httpx import AsyncClient
from pytest_redis import factories

from app.asgi import get_asgi_application
from app.redis import get_redis
from app.settings import settings


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield get_asgi_application()


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url='http://testserver') as c:
        yield c


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


redis_in_docker = factories.redis_noproc(**{
    'host': settings.REDIS_HOST,
    'port': settings.REDIS_PORT,
})


@pytest.fixture(scope='session', autouse=True)
async def redis_client(redis_in_docker, event_loop):
    yield redis.Redis(**{
        'host': redis_in_docker.host,
        'port': redis_in_docker.port,
    })


@pytest.fixture(scope='function', autouse=True)
async def clear_redis(redis_client):
    for key in redis_client.scan_iter('*'):
        redis_client.delete(key)
    yield
    for key in redis_client.scan_iter('*'):
        redis_client.delete(key)


@pytest.fixture(scope='function', autouse=True)
async def session_override(app, redis_client):
    async def get_redis_override():
        return redis_client

    app.dependency_overrides[get_redis] = get_redis_override
