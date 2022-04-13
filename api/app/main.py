from fastapi import FastAPI
import uvicorn
import asyncio

try:
    from src import startup
except ImportError:
    from .src import startup

app = FastAPI()
startup.initRoutes(app)
startup.resetTimers()

if __name__ == '__main__':
    asyncio.run(uvicorn.run(app, port=8000, host='0.0.0.0'))
