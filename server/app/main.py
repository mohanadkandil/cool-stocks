from fastapi import FastAPI
import uvicorn
#from .src import cmb
from src import db
from src import routers

def conndb() -> None:
    db.Base.metadata.create_all(bind=db.engine)

def routes(app):
    app.include_router(routers.stockRouter,prefix="/db/stock",tags=["Stock Queries"])
    app.include_router(routers.userRouter,prefix="/db/user",tags=["User Queries"])
    app.include_router(routers.transRouter,prefix="/db/transaction",tags=["Transaction Queries"])

app = FastAPI()
routes(app)
conndb()

if __name__ == '__main__':
    uvicorn.run(app, port=80, host='0.0.0.0')