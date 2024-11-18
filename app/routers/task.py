
import os
import sys
from fastapi import APIRouter, Depends, Path, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Аннотации, Модели БД и Pydantic.
from typing import Annotated, List
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.db_depends import get_db
from models.task import Task
from models.user import User
from schemas.schemas import CreateTask, TaskResponse, UserResponse, UpdateTask



router = APIRouter(prefix='/task', tags=['task'])



@router.get('/', response_model=List[TaskResponse])
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    if not tasks:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There are not tasks')
    return tasks



# scalar() вместо scalars(), чтобы получить единственное значение и без .all()
@router.get('/{task_id}', response_model=UserResponse)
async def task_by_id(user_id: Annotated[int, Path(ge=1, le=100, description='Enter id', example='15')],
                     db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(Task).where(Task.id == user_id))
    if not user:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is not user')
    return user



@router.post('/create/{user_id}', status_code=201)
async def create_task(user_id: Annotated[int, Path(ge=1, le=100, description='Enter id', example='15')],
                     db: Annotated[Session, Depends(get_db)], create_task: CreateTask):
    # Проверка на существование пользователя с таким же id
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is not user')
    # # Проверка на существование задачи с таким же названием для данного пользователя
    existing_task = db.scalar(select(Task).where(Task.title == create_task.title, Task.user_id == user_id))
    if existing_task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Task already exists for this user')
    # Создание новой задачи
    db.execute(insert(Task).values(title=create_task.title,
                                    content=create_task.content,
                                    priority=create_task.priority,
                                    slug=slugify(create_task.title),
                                    user_id=user_id))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update/{task_id}', status_code=200)
async def update_task(task_id: Annotated[int, Path(ge=1, le=100, description='Enter id', example='15')],
                     db: Annotated[Session, Depends(get_db)], 
                     update_task: UpdateTask):
    # поиск задачи
    task_update = db.scalar(select(Task).where(Task.id == task_id))
    if task_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no task found')
    # Обновление задачи
    db.execute(update(Task).where(Task.id == task_id).values(title=update_task.title,
                                                            content=update_task.content,
                                                            priority=update_task.priority,
                                                            slug=slugify(update_task.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task updatind is successful!'}



@router.delete('/delete/{task_id}', status_code=200)
async def delete_task(task_id: Annotated[int, Path(ge=1, le=100, description='Enter id', example='15')],
                     db: Annotated[Session, Depends(get_db)]):
    task_delete = db.scalar(select(Task).where(Task.id == task_id))
    if task_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful'}
