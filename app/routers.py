from fastapi import FastAPI

from routers import DomainRouter, LinksRouter


def add_routers(app: FastAPI):
    app.include_router(**{
        'router': LinksRouter.router,
        'prefix': '/api',
    })
    app.include_router(**{
        'router': DomainRouter.router,
        'prefix': '/api',
    })

    return app
