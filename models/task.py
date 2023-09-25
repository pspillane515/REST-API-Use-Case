from db import db


class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    details = db.Column(db.String, unique=False, nullable=True)
    completed = db.Column(db.Boolean, unique=False, nullable=True)

    todolist_id = db.Column(
        db.Integer, db.ForeignKey("todolists.id"), unique=False, nullable=False
    )
    todolist = db.relationship("TodoListModel", back_populates="tasks")

    categories = db.relationship("CategoryModel", back_populates="tasks", secondary="tasks_categories")
