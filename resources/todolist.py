import uuid 
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TodoListModel
from schemas import TodoListSchema

blp = Blueprint("TodoLists", __name__, description="Operations on todolists")



@blp.route("/todolist/<int:todolist_id>")
class TodoList(MethodView):
    @blp.response(200, TodoListSchema)
    def get(self, todolist_id):
        todolist = TodoListModel.query.get_or_404(todolist_id)
        return todolist

    def delete(self, todolist_id):
        todolist = TodoListModel.query.get_or_404(todolist_id)
        db.session.delete(todolist)
        db.session.commit()
        return {"Message": "TodoList deleted"}


@blp.route("/todolist")
class TodoListList(MethodView):
    @blp.response(200, TodoListSchema(many=True))
    def get(self):
        return TodoListModel.query.all()
    
    @blp.arguments(TodoListSchema)
    @blp.response(201, TodoListSchema)
    def post(self, todolist_data):
        todolist = TodoListModel(**todolist_data)

        try:
            db.session.add(todolist)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A TodoList with that name already exists."
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the todolist.")
        
        return todolist