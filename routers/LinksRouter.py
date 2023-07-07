import re
import time
import uuid
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, status
from redis.client import Redis
from redis.commands.json.path import Path

from app.redis import get_redis
from responses.GeneralJsonResponse import GeneralJsonResponse
from schemas.LinksSchema import LinksSchema

router = APIRouter()


@router.post('/visited_links')
async def create_visited_links(
        data: LinksSchema,
        redis: Redis = Depends(get_redis),
) -> GeneralJsonResponse:
    if not data.links:
        return GeneralJsonResponse(**{
            'status_msg': 'Links is empty.',
            'status_code': status.HTTP_400_BAD_REQUEST,
        })

    created_at = int(time.time())
    links = set()

    for link in data.links:
        url = urlparse(link)

        if url.netloc:
            links.add(url.netloc)
        else:
            pattern = r'(?P<domain>[\w\-]+\.+[\w\-]+)'
            match = re.search(pattern, link)

            if not match:
                return GeneralJsonResponse(**{
                    'status_msg': 'Url is not valid.',
                    'status_code': status.HTTP_400_BAD_REQUEST,
                })

            domain = match.group('domain')
            links.add(domain)

    key = f'links:{uuid.uuid4()}'
    value = {
        'created_at': created_at,
        'links': list(links),
    }

    redis.json().set(key, Path.root_path(), value)

    return GeneralJsonResponse(**{
        'status_msg': 'ok',
        'status_code': status.HTTP_201_CREATED,
    })
