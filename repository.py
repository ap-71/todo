from abc import abstractmethod
from pydantic import BaseModel
from sqlalchemy import desc
from db import get_session
from models import Task, TaskUser
from schemas import TaskCreateSchema, UserSchema, TaskSchema


class Repository:
    @abstractmethod
    def add(self, schema: BaseModel) -> BaseModel:
        pass
    
    @abstractmethod
    def get(self) -> list[BaseModel]:
        pass
    
    @abstractmethod
    def update(self, id_: int, **kwargs) -> BaseModel:
        pass
    
    @abstractmethod
    def delete(self, id_: int) -> None:
        pass


class TaskRepository(Repository):
    def __init__(self, user: UserSchema) -> None:
        self.user = user
    
    def add(self, schema: TaskCreateSchema) -> TaskSchema:
        with get_session()as session:
            task_ = Task(title=schema.title, description=schema.description)
            session.add(task_)
            session.commit()
            
            task_user_ = TaskUser(task_id=task_.id, user_id=self.user.id)
            session.add(task_user_)
            session.commit()
            
            task = TaskSchema(id=task_.id, **schema.model_dump())
            
        return task
            
    
    def get(self, id_: int | None = None, is_deleted=False) -> list[TaskSchema]:
        with get_session()as session:
            filters = [
                Task.task_user.has(TaskUser.user_id==self.user.id),
                Task.is_deleted==is_deleted
            ]
            
            if id_ is not None:
                filters.append(Task.id==id_)
                
            tasks: list[Task] = session.query(Task).filter(*filters).order_by(desc(Task.dt_add)).all()
        
        tasks_: list[TaskSchema] = []
        for task in tasks:
            tasks_.append(TaskSchema.model_validate(task.__dict__))
            
        return tasks_
    
    def update(self, id_: int, title: str | None = None, description: str | None = None):
        with get_session()as session:
            session.query(Task).filter(Task.id==id_).update({Task.title: title, Task.description: description})
            session.commit()
    
    def delete(self, id_: int):
        with get_session()as session:
            session.query(Task).filter(Task.id==id_).delete()
            session.commit()
        