from datetime import datetime
from typing import Optional
from sqlalchemy import UniqueConstraint, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from db import engine


class Base(DeclarativeBase):
    """базовая модель"""

    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String(120))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
    task_user: Mapped["TaskUser"] = relationship(back_populates="user")
    task_user_comment: Mapped["TaskUserComment"] = relationship(back_populates="user")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(String(250))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
    task_user: Mapped["TaskUser"] = relationship(back_populates="task")
    task_tag: Mapped["TaskTag"] = relationship(back_populates="task")
    task_user_comment: Mapped["TaskUserComment"] = relationship(back_populates="task")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    task_tag: Mapped["TaskTag"] = relationship(back_populates="tag")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(512))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
    task_user_comment: Mapped["TaskUserComment"] = relationship(back_populates="comment")
    

class TaskUserComment(Base):
    __tablename__ = "task_user_comment"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
    task: Mapped[Task] = relationship(back_populates="task_user_comment")
    user: Mapped[User] = relationship(back_populates="task_user_comment")
    comment: Mapped[Comment] = relationship(back_populates="task_user_comment")
    
    __table_args__ = (UniqueConstraint(task_id, user_id, comment_id, name="unique__task_id__user_id__comment_id"),)


class TaskTag(Base):
    __tablename__ = "task_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
    task: Mapped[Task] = relationship(Task, back_populates="task_tag")
    tag: Mapped[Tag] = relationship(Tag, back_populates="task_tag")

    __table_args__ = (UniqueConstraint(task_id, tag_id, name="unique__task_id__tag_id"),)


class TaskUser(Base):
    __tablename__ = "task_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    dt_add: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
    task: Mapped[Task] = relationship(back_populates="task_user")
    user: Mapped[User] = relationship(back_populates="task_user")
    
    __table_args__ = (UniqueConstraint(task_id, user_id, name="unique__task_id__user_id"),)


Base.metadata.create_all(bind=engine)
