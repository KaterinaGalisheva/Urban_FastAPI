import sys
import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.db import Base





class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    tasks = relationship("Task", back_populates="user")

    
'''# проверка создания таблицы
from sqlalchemy.schema import CreateTable
print(CreateTable(User.__table__))'''