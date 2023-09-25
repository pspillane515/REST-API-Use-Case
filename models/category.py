from db import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    todolist_id = db.Column(db.Integer, db.ForeignKey("todolists.id"), nullable=False) 

    todolist = db.relationship("TodoListModel", back_populates="categories")
    tasks = db.relationship("TaskModel", back_populates="categories", secondary="tasks_categories")