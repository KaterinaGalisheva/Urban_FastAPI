
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
from schemas.schemas import CreateUser, UpdateUser, UserResponse




router = APIRouter(prefix='/user', tags=['user'])

# Каждая из нижеперечисленных функций подключается к базе данных в момент обращения при помощи 
# функции get_db - Annotated[Session, Depends(get_db)]

@router.get('/', response_model=List[UserResponse])
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    if not users:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There are not users')
    return users



# scalar() вместо scalars(), чтобы получить единственное значение и без .all()
@router.get('/{user_id}', response_model=UserResponse)
async def user_by_id(user_id: Annotated[int, Path(ge=1, le=100, description='Enter id', example='15')],
                     db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is not user')
    return user



@router.post('/create', status_code=201)
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    # Проверка на существование пользователя с таким же именем
    existing_user = db.scalar(select(User).where(User.username == create_user.username))
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already exists')
    # Создание нового пользователя
    db.execute(insert(User).values(username=create_user.username,
                                      firstname=create_user.firstname,
                                      lastname=create_user.lastname,
                                      age=create_user.age,
                                      slug=slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}



@router.put('/update/{user_id}', status_code=200)
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter id', example='15')],
                     db: Annotated[Session, Depends(get_db)], 
                     update_user: UpdateUser):
    # поиск пользователя
    user_update = db.scalar(select(User).where(User.id == user_id))
    if user_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no user found')
    # Обновление пользователя
    db.execute(update(User).where(User.id == user_id).values(username=update_user.username,
                                                            firstname=update_user.firstname,
                                                            lastname=update_user.lastname,
                                                            age=update_user.age,
                                                            slug=slugify(update_user.username)))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User updatind is successful!'}



@router.delete('/delete/{user_id}', status_code=200)
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter id', example='15')],
                      db: Annotated[Session, Depends(get_db)]):
    user_delete = db.scalar(select(User).where(User.id == user_id))
    if user_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful'}
#вместе с пользователем удалялись все задачи связанные с ним



@router.get ("/user_id/tasks/{user_id}", response_model=List[UserResponse])
async def tasks_by_user_id(user_id: Annotated[int, Path(ge=1, le=100, description='Enter id', example='15')],
                           db: Annotated[Session, Depends(get_db)]):
    # Получаем задачи для конкретного пользователя
    tasks_for_user = db.execute(select(Task).where(Task.user_id==user_id)).scalars().all()
    if not tasks_for_user:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There are not tasks for user')
    return tasks_for_user
    
 

  
    