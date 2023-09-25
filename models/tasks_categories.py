from db import db


class TaskCategories(db.Model):
    __tablename__ = "tasks_categories"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))