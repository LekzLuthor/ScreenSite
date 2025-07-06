import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import items  # ваш API-роутер

app = FastAPI()

# 1) Генерим таблицы в БД при старте (как раньше)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 2) Подключаем CORS (если нужно, для API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ваш фронт-домен
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3) Монтируем статику на абсолютный корень
#    html=True означает: при незнакомом пути возвращай index.html (SPA fallback)
app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static",
)

# 4) Подключаем все API-роуты под префиксом `/api` (рекомендуется)
#    Тогда фронт-код будет посылать запросы на `/api/items` и пр.
app.include_router(items.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
