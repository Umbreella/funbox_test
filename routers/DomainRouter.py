import json

from fastapi import APIRouter, Depends, status
from redis.client import Redis

from app.redis import get_redis
from responses.GeneralJsonResponse import GeneralJsonResponse

router = APIRouter()


@router.get('/visited_domains')
async def get_visited_domains(
        from_: int,
        to: int,
        redis: Redis = Depends(get_redis),
) -> GeneralJsonResponse:
    query = f'@created_at:[{from_} {to}]'
    result = redis.ft().search(query)

    domains = set()

    for doc in result.docs:
        links = json.loads(doc.json)

        domains.update(links.get('links', []))

    return GeneralJsonResponse(**{
        'data': {
            'domains': list(domains),
        },
        'status_msg': 'ok',
        'status_code': status.HTTP_200_OK,
    })
