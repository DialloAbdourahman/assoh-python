from mongoengine import StringField, EmbeddedDocument

class Address(EmbeddedDocument):
    country = StringField(required=False)
    city = StringField(required=False)
    street_name = StringField(required=False)
    street_number = StringField(required=False)
    postal_code  = StringField(required=False)



