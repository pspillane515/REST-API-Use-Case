from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TaskModel
from schemas import TaskSchema, TaskUpdateSchema

blp = Blueprint("Tasks", __name__, description="Operations on tasks")



@blp.route("/item/<int:item_id>")
class Task(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, item_id):
        item = TaskModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        item = TaskModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"Message": "Task.deleted"}

    @blp.arguments(TaskUpdateSchema)
    @blp.response(200, TaskSchema)
    def put(self, item_data, item_id):
        item = TaskModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = TaskModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        return item

@blp.route("/item")
class TodoList(MethodView):
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        return TaskModel.query.all()
    
    @jwt_required(fresh=True)
    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, item_data):
        item= TaskModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        
        return item