from fastapi import APIRouter

welcomeRouter = APIRouter()

@welcomeRouter.get('/', status_code=200)
def get():
    return {'message': 'Welcome to thndr main app'}