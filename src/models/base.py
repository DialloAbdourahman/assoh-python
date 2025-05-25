from mongoengine import Document, DateTimeField, BooleanField, ReferenceField

class BaseModel(Document):
    created_at = DateTimeField(required=True)
    # created_by = ReferenceField()
    updated_at = DateTimeField()
    # updated_by = ReferenceField()
    deleted_at = DateTimeField()
    # deleted_by = ReferenceField()
    deleted = BooleanField(default=False, required=True)
