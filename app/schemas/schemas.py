from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

class UpdateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int


class CreateTask(BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int


# для корректных возвращаемых ответов. 
# Так как таблицы TASK USER наследуются от алхимии

class TaskResponse(BaseModel):
    id: int
    title: str
    content: str
    priority: int
    slug: str
    user_id: int

    class Config:
        from_attributes = True  # Позволяет Pydantic работать с ORM-объектами


class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str

    class Config:
        from_attributes = True  # Позволяет использовать ORM-модели





'''Зачем используется Pydantic?
Pydantic используется вместо SQLAlchemy по следующим причинам:

Валидация данных: Pydantic автоматически проверяет и валидирует входящие данные на соответствие определенным типам. 
Например, если вы попытаетесь создать пользователя с нестроковым значением для username, Pydantic выбросит ошибку валидации. 
Это особенно полезно для API, где необходимо убедиться, что данные, полученные от клиента, корректны.

Сериализация и десериализация: Pydantic упрощает процесс преобразования данных между форматами, такими как JSON и Python-объекты. 
Это делает его идеальным для работы с API, где данные часто передаются в формате JSON.

Читаемость и поддержка: Определение моделей с помощью Pydantic делает код более понятным и структурированным. 
Это облегчает поддержку и расширение кода в будущем.

Отделение логики валидации от логики базы данных: Используя Pydantic для валидации данных, вы можете отделить логику валидации от логики работы с базой данных, 
которая обычно реализуется с помощью SQLAlchemy. Это улучшает организацию кода и делает его более модульным.

Заключение
Таким образом, код, представленный выше, определяет модели для создания и обновления пользователей и задач, 
используя Pydantic для валидации и сериализации данных. Это позволяет обеспечить корректность входящих данных и улучшить структуру приложения, 
отделяя логику валидации от работы с базой данных, которая может быть реализована с помощью SQLAlchemy или других ORM.'''