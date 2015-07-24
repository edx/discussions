"""
Models for the discussions app.
"""
from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    IntField,
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


class Contents(Document):
    class Votes(EmbeddedDocument):
        """Represents threads read by the user."""
        up = ListField()  # TODO Double check this
        down = ListField()  # TODO Double check this
        up_count = IntField()
        down_count = IntField()
        count = IntField()
        point = IntField()

    _id = ObjectIdField(required=True, primary_key=True)
    votes = DictField(required=True)
    visible = BooleanField(required=True)
    abuse_flaggers = ListField()  # TODO Double check this
    historical_abuse_flaggers = ListField()  # TODO Double check this
    thread_type = StringField(required=True)  #TODO Can this be a ChoiceField?
    comment_count = IntField(required=True)
    at_position_list = ListField()  # TODO Double check this
    title = StringField(required=True)
    body = StringField(required=True)
    course_id = StringField(required=True)  # TODO Could we add a course id validator here?
    commentable_id = StringField(required=True)
    _type = StringField(required=True)  #TODO Can this be a ChoiceField?
    anonymous = StringField(required=True)  # This is a boolean string -.-
    anonymous_to_peers = StringField(required=True)  # This is a boolean string -.-
    closed = StringField(required=True)  # This is a boolean string -.-
    author_id = StringField(required=True)  # This is a int string -.-
    author_username = StringField(required=True)
    updated_at = DateTimeField(required=True)  # TODO is this DateTime
    created_at = DateTimeField(required=True)  # TODO is this DateTime
    last_activity_at = DateTimeField(required=True)  # TODO is this DateTime
    comment_thread_id = StringField()  # TODO I didn't see this in my database query
    parent_ids = ListField()  # TODO I didn't see this in my database query
    sk = StringField()  # TODO I didn't see this in my database query
    endorsed = BooleanField()  # TODO I didn't see this in my database query


class Subscriptions(Document):
    _id = ObjectIdField(required=True, primary_key=True)
    subscriber_id = StringField(required=True)  # This is a int string -.-
    source_id = StringField(required=True)  # This is a int string -.-
    source_type = StringField(required=True)  #TODO Can this be a ChoiceField?
    updated_at = DateTimeField(required=True)  # TODO is this DateTime
    created_at = DateTimeField(required=True)  # TODO is this DateTime


