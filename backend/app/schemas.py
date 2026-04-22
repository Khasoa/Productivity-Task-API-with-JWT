from marshmallow import Schema, fields

class UserSchema(Schema):
    """Serializer for safe user output — never exposes password_hash."""
    id = fields.Int(dump_only=True)
    username = fields.Str()

class TaskSchema(Schema):
    """Serializer for task output."""
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    completed = fields.Bool()
    priority = fields.Str()
    created_at = fields.DateTime()
    user_id = fields.Int(dump_only=True)  # Read-only — set server-side from JWT


# Pre-instantiated for reuse across routes
user_schema = UserSchema()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)