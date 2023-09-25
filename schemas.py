from marshmallow import Schema, fields

class PlainTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    details = fields.Str(required=False)
    completed = fields.Bool(required=False)

class PlainTodoListSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class TaskSchema(PlainTaskSchema):
    todolist_id = fields.Int(required=True, load_only=True)
    todolist = fields.Nested(PlainTodoListSchema(), dump_only=True)
    categories = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)

class TaskUpdateSchema(Schema):
    name = fields.Str()
    details = fields.Str()
    completed = fields.Bool()

class TodoListUpdateSchema(Schema):
    name = fields.Str()

class TodoListSchema(PlainTodoListSchema):
    tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)
    categories = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)
    user_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)

class CategorySchema(PlainCategorySchema):
    todolist_id = fields.Int(load_only=True)
    tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)
    todolist = fields.Nested(PlainTodoListSchema(), dump_only=True)

class CategoryAndTaskSchema(Schema):
    message = fields.Str()
    task = fields.Nested(TaskSchema)
    category = fields.Nested(CategorySchema)

class UserSchema(PlainUserSchema):
    todolist = fields.List(fields.Nested(PlainTodoListSchema(), dump_only=True))
