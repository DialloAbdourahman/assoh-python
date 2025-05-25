from mongoengine import Document, DateTimeField, BooleanField
from datetime import datetime

class BaseModel(Document):
    meta = {'abstract': True}  

    created_at = DateTimeField(required=True, default=datetime.utcnow())
    # created_by = ReferenceField()
    updated_at = DateTimeField()
    # updated_by = ReferenceField()
    deleted_at = DateTimeField()
    # deleted_by = ReferenceField()
    deleted = BooleanField(default=False, required=True)
