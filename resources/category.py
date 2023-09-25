from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CategoryModel, TodoListModel, TaskModel
from schemas import CategorySchema, CategoryAndTaskSchema

blp = Blueprint("Categories", "categories", description="Operations on categories")


@blp.route("/todolist/<string:todolist_id>/category")
class CategorysInTodoList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self, todolist_id):
        todolist = TodoListModel.query.get_or_404(todolist_id)

        return todolist.categories.all()  # lazy="dynamic" means 'categories' is a query

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data, todolist_id):
        if CategoryModel.query.filter(CategoryModel.todolist_id == todolist_id, CategoryModel.name == category_data["name"]).first():
            abort(400, message="A category with that name already exists in that todolist.")

        category = CategoryModel(**category_data, todolist_id=todolist_id)

        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return category


@blp.route("/task/<string:task_id>/category/<string:category_id>")
class LinkCategoriesToTask(MethodView):
    @blp.response(201, CategorySchema)
    def post(self, task_id, category_id):
        task = TaskModel.query.get_or_404(task_id)
        category = CategoryModel.query.get_or_404(category_id)

        task.categories.append(category)

        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")

        return category

    @blp.response(200, CategoryAndTaskSchema)
    def delete(self, task_id, category_id):
        task = TaskModel.query.get_or_404(task_id)
        category = CategoryModel.query.get_or_404(category_id)

        task.categories.remove(category)

        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")

        return {"message": "task removed from category", "task": task, "category": category}


@blp.route("/category/<string:category_id>")
class category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    @blp.response(
        202,
        description="Deletes a category if no task is categorized with it.",
        example={"message": "category deleted."},
    )
    @blp.alt_response(404, description="category not found.")
    @blp.alt_response(
        400,
        description="Returned if the category is assigned to one or more tasks. In this case, the category is not deleted.",
    )
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)

        if not category.tasks:
            db.session.delete(category)
            db.session.commit()
            return {"message": "category deleted."}
        abort(
            400,
            message="Could not delete category. Make sure category is not associated with any tasks, then try again.",  # noqa: E501
        )
