'''from contextlib import asynccontextmanager'''
import os
import sys
from fastapi import FastAPI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from .routers import user, task
import uvicorn

'''from backend.db import create_tables, delete_tables'''

'''
Удобное создание таблиц для отладки кода, таблицы в этом проекте создаются в evn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База создана и готова к работе')
    yield
    print('Выключение')
    '''


#app = FastAPI(lifespan=lifespan)   если используется код выше
app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to Taskmanager"}

#Подключение роутеров из других файлов
app.include_router(task.router)
app.include_router(user.router)

# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
'''dependencies=[Depends(verify_token), Depends(verify_key)]: Этот параметр dependencies указывает, 
что все маршруты, определенные в этом экземпляре приложения, будут использовать указанные зависимости.
при каждом запросе к любому маршруту в этом приложении будут автоматически вызываться функции verify_token и verify_key, 
что позволяет реализовать централизованную логику аутентификации и авторизации. Если одна из этих зависимостей не пройдет проверку, запрос может быть отклонен до того, 
как будет достигнут обработчик маршрута.'''





# Запуск сервера осуществите командой, приложение начнет работать на странице
# python -m uvicorn main:app
# или в режиме релоуда (перезапуск при изменениях)
# uvicorn app.main:app --reload
# или в режиме отладки
# uvicorn app.main:app --reload --log-level debug

# Инициализация Alembic в конкретной папке
# alembic init app/migrations

# миграция 
# alembic revision --autogenerate -m "Initial migration"

# Выполните команду 
# alembic upgrade head
# которая позволит вам применить последнюю миграцию и создать таблицы User, Task и запись текущей версии миграции если таблицы создаются в файле evn

