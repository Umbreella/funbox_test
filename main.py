import uvicorn

from app.asgi import get_asgi_application

if __name__ == '__main__':
    app = get_asgi_application()

    uvicorn.run(app)
