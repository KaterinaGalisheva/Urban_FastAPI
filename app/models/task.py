import sys
import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.db import Base
from models.user import User




class Task(Base):
    __tablename__ = 'tasks' #указывает имя таблицы в базе данных, которая будет соответствовать этому классу
    id = Column(Integer, primary_key=True, index=True) #Каждый атрибут класса соответствует столбцу в таблице базы данных:
    # Column — это функция, которая определяет столбец в таблице.
    #Integer — тип данных столбца.
    #primary_key=True указывает, что этот столбец является первичным ключом.
    #index=True создает индекс для этого столбца, что ускоряет поиск по нему.
    title = Column(String)
    content = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False) #По умолчанию значение False
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    # ForeignKey("users.id") указывает, что этот столбец является внешним ключом, ссылающимся на столбец id в таблице users.
    # nullable=False означает, что это поле обязательно для заполнения.
    # index=True создает индекс для этого столбца.
    slug = Column(String, unique=True, index=True)
    user = relationship("User", back_populates="tasks")
    # relationship устанавливает связь между моделью Task и моделью User . Это позволяет SQLAlchemy автоматически загружать связанные объекты.
    # back_populates="tasks" указывает, что в модели User  также будет связь, которая ссылается на tasks. Это создает двустороннюю связь между задачами и пользователями.


'''# проверка создания таблицы, можно использовать при необходимости
from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))'''