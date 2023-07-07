from fastapi import FastAPI
from redis.commands.search.field import NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.exceptions import ResponseError

from app.redis import redis_cli


def get_asgi_application():
    app = FastAPI()

    try:
        redis_cli.ft().info()
    except ResponseError:
        redis_cli.ft().create_index(**{
            'fields': (
                NumericField("$.created_at", as_name="created_at"),
            ),
            'definition': IndexDefinition(**{
                'prefix': ['links:', ],
                'index_type': IndexType.JSON,
            }),
        })

    return app
