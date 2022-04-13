from .. import routers
from .. import error

def initRoutes(app):
    app.include_router(routers.welcomeRouter,prefix="",tags=["welcome"])
    app.include_router(routers.userRouter,prefix="/user",tags=["user"])
    app.include_router(routers.stockRouter,prefix="/stock",tags=["stock"])

    app.middleware('http')(error.catch_exceptions_middleware)