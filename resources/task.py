from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TaskModel
from schemas import TaskSchema, TaskUpdateSchema

blp = Blueprint("Tasks", "tasks", description="Operations on tasks")


@blp.route("/task/<string:task_id>")
class task(MethodView):
    @jwt_required()
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task

    @jwt_required()
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "task deleted."}

    @blp.arguments(TaskUpdateSchema)
    @blp.response(200, TaskSchema)
    def put(self, task_data, task_id):
        task = TaskModel.query.get(task_id)

        if task:
            task.details = task_data["details"]
            task.name = task_data["name"]
            task.completed = task_data["completed"]
            task.todolist_id = task_data["todolist_id"]
        else:
            task = TaskModel(id=task_id, **task_data)

        db.session.add(task)
        db.session.commit()

        return task


@blp.route("/task")
class taskList(MethodView):
    @jwt_required()
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        return TaskModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        task = TaskModel(**task_data)

        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the task.")

        return task
