from fastapi import FastAPI
from redis.commands.search.field import NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.exceptions import ResponseError

from app.redis import redis_cli
from app.routers import add_routers


def get_asgi_application():
    app = FastAPI(**{
        'docs_url': '/api/docs/',
        'openapi_url': '/api/docs/json/',
    })

    try:
        redis_cli.ft().info()
    except ResponseError:
        redis_cli.ft().create_index(**{
            'fields': (
                NumericField('$.created_at', as_name='created_at'),
            ),
            'definition': IndexDefinition(**{
                'prefix': ['links:', ],
                'index_type': IndexType.JSON,
            }),
        })

    add_routers(app)

    return app
