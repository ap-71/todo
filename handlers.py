from flask import Response, redirect, render_template, request, url_for, session
from db import get_session
from init import app
from models import Task, TaskUser
from repository import TaskRepository
from schemas import LoginSchema, TaskCreateSchema, TaskSchema, UserSchema

def check_access(func):
    def wrap(*args, **kwargs):
        user_data = session.get('user', None)
        
        if user_data is None:
            return redirect(url_for(login.__name__))
        
        current_user = UserSchema.model_validate_json(user_data)
        
        return func(*args, current_user=current_user, **kwargs)
    
    wrap.__name__ = func.__name__
    
    return wrap

@app.route('/')
@check_access
def main(current_user: UserSchema):
    task_repo = TaskRepository(user=current_user)
    tasks: list[TaskSchema] = task_repo.get()
        
    return render_template('tasks.html', tasks=tasks, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    current_user: UserSchema | None = None 
    user_data: str | None = session.get('user', None)
    referrer = request.referrer
        
    if request.method == 'POST':
        referrer = None
        user_data = None
        session.clear()
        
        login = LoginSchema.model_validate(request.form.to_dict())
        current_user = login.get_user()    
    
    if user_data is not None and current_user is None:
        current_user = UserSchema.model_validate_json(user_data)
        
    if current_user is not None:
        session.update(user=current_user.model_dump_json())
        return redirect(url_for(referrer or main.__name__))
    
    return render_template('login.html')


@app.route("/tasks/add", methods=['GET', 'POST'])
@check_access
def add_task(current_user: UserSchema):
    if request.method == 'POST':
        task = TaskCreateSchema.model_validate(request.form.to_dict())
        
        TaskRepository(user=current_user).add(task)
        
        return redirect(url_for(main.__name__))
    
    return render_template('tasks_add.html', current_user=current_user)


@app.route("/tasks/<task_id>", methods=['GET'])
@check_access
def get_task(current_user: UserSchema, task_id: int):
    # task_id: int = int(request.args['task_id'])
    task_repo = TaskRepository(user=current_user)
    current_task = task_repo.get(task_id)
    
    if current_task is None or current_task.__len__() == 0:
        return redirect(url_for(main.__name__))
    
    return render_template('task_detail.html', current_user=current_user, task=current_task[0])