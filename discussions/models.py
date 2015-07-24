"""
Models for the discussions app.
"""
from mongoengine import (
    DictField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    ListField,
    ObjectIdField,
    StringField
)


class User(Document):
    """Represents a user."""
    class ReadState(EmbeddedDocument):
        """Represents threads read by the user."""
        _id = ObjectIdField(required=True)
        # TODO These values in this dict need to be validated
        last_read_times = DictField(required=True)
        course_id = StringField(required=True)

    meta = {
        'collection': 'users',
        'index_background': True,
        'indexes': [
            'external_id'
        ]
    }

    external_id = StringField(required=True, unique=True)
    _id = StringField(default=external_id, required=True, primary_key=True)
    username = StringField(required=True)
    default_sort_key = StringField(default='date', required=True)
    read_states = EmbeddedDocumentListField(ReadState, required=True)
    # TODO: implement notification model and set up has_and_belongs_to_many
    # relationship as defined in comments_service
    notification_ids = ListField(required=True)
