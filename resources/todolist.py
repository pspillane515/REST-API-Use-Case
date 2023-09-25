from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from models import TodoListModel, UserModel
from schemas import TodoListSchema, TodoListUpdateSchema


blp = Blueprint("To-do Lists", "todolists", description="Operations on todolists")


@blp.route("/todolist/<string:todolist_id>")
class TodoList(MethodView):
    @jwt_required()
    @blp.response(200, TodoListSchema)
    def get(self, todolist_id):
        todolist = TodoListModel.query.get_or_404(todolist_id)
        current_user = get_jwt_identity()
        if not todolist.user_id == current_user:
            abort(400, message="You are not the owner of that to-do list.")
        return todolist

    @jwt_required()
    def delete(self, todolist_id):
        todolist = TodoListModel.query.get_or_404(todolist_id)
        current_user = get_jwt_identity()
        if not todolist.user_id == current_user:
            abort(400, message="You do not currently have permission to delete a to-do list for that user.")
        db.session.delete(todolist)
        db.session.commit()
        current_user = get_jwt_identity()
        return {"message": f"todolist deleted for user_id: {current_user}"}, 200
    
    @jwt_required
    @blp.arguments(TodoListUpdateSchema)
    @blp.response(200, TodoListSchema)
    def put(self, todolist_data, todolist_id):
        tasklist = TodoListModel.query.get(todolist_id)

        if tasklist:
            tasklist.name = todolist_data["name"]
        else:
            tasklist = TodoListModel(id=todolist_id, **todolist_data)
        db.session.add(tasklist)
        db.session.commit()

        return tasklist

@blp.route("/todolist")
class todolistList(MethodView):
    @jwt_required(optional=True)
    @blp.response(200, TodoListSchema(many=True))
    def get(self):
        # current_user = get_jwt_identity()
        # return {"message": f"The current user is: {current_user}"}
        # return TodoListModel.query.filter(TodoListModel.user_id == current_user).all()
        return TodoListModel.query.all()

    @jwt_required()
    @blp.arguments(TodoListSchema)
    @blp.response(201, TodoListSchema)
    def post(self, todolist_data):
        todolist = TodoListModel(**todolist_data)
        current_user = get_jwt_identity()
        if not todolist.user_id == current_user:
            abort(400, message="You do not currently have permission to create a to-do list for that user.")
        try:
            db.session.add(todolist)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A todolist with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the todolist.")

        return todolist
