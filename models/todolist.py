from db import db

class TodoListModel(db.Model):
    __tablename__ = "todolists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
 
    users = db.relationship("UserModel", back_populates="todolist")
    tasks = db.relationship("TaskModel", back_populates="todolist", lazy="dynamic", cascade="all, delete")
    categories = db.relationship("CategoryModel", back_populates="todolist", lazy="dynamic", cascade="all, delete")