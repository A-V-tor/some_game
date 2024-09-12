import uvicorn
from fastapi import FastAPI
from sqladmin import Admin
from src.api_v1.routes import router
from src.database.base import engine
from src.admin import PlayerView, PlayerLevelView, PrizeView, LevelView, LevelPrizeView, BoostView


def create_web_app():
    app = FastAPI(docs_url='/docs')
    app.include_router(router)

    admin = Admin(app=app, engine=engine)
    admin.add_view(PlayerView)
    admin.add_view(PlayerLevelView)
    admin.add_view(PrizeView)
    admin.add_view(LevelView)
    admin.add_view(LevelPrizeView)
    admin.add_view(BoostView)

    return app


if __name__ == '__main__':
    uvicorn.run(f'{__name__}:create_web_app', host='0.0.0.0', reload=True)
