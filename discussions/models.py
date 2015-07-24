"""
Models for the discussions app.
"""
from mongoengine import (
    BooleanField,
    DateTimeField,
    DictField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    IntField,
    ListField,
    ObjectIdField,
    StringField,
    queryset_manager
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
    read_states = EmbeddedDocumentListField(ReadState, default=[])
    # TODO: implement notification model and set up has_and_belongs_to_many
    # relationship as defined in comments_service
    notification_ids = ListField(default=[])


class Content(Document):
    """Base collection for Comment and CommentThread."""
    meta = {
        'abstract': True
    }

    class Votes(EmbeddedDocument):
        """Represents votes on content."""
        up = ListField()
        down = ListField()
        up_count = IntField(default=0)
        down_count = IntField(default=0)
        count = IntField(default=0)
        point = IntField(default=0)

    visible = BooleanField(default=True)
    abuse_flaggers = ListField(default=[])
    historical_abuse_flaggers = ListField(default=[])
    author_username = StringField(default=None)
    course_id = StringField()
    body = StringField()
    anonymous = BooleanField(default=False)
    anonymous_to_peers = BooleanField(default=False)
    at_position_list = ListField()
    votes = EmbeddedDocumentField(Votes)
    created_at = DateTimeField()
    updated_at = DateTimeField()
    author_id = StringField()


class CommentThread(Content):
    """Represents a Thread."""
    meta = {'collection': 'contents'}
    _type = StringField(default='CommentThread')
    thread_type = StringField(default='discussion', choices=['question', 'discussion'])
    comment_count = IntField(default=0)
    title = StringField()
    commentable_id = StringField()
    closed = BooleanField(default=False)
    last_activity_at = DateTimeField()
    group_id = IntField()
    pinned = BooleanField()

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset(_type='CommentThread')


class Comment(Content):
    """Represents a Comment."""
    meta = {'collection': 'contents'}
    _type = StringField(default='Comment')
    endorsed = BooleanField(default=False)
    endorsement = DictField()
    sk = StringField(default=None)
    comment_thread_id = ObjectIdField()
    parent_ids = ListField()

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset(_type='Comment')


class Subscription(Document):
    _id = ObjectIdField(required=True, primary_key=True)
    subscriber_id = StringField(required=True)
    source_id = StringField(required=True)
    source_type = StringField(required=True)  #TODO Can this be a ChoiceField?
    updated_at = DateTimeField(required=True)  # TODO is this DateTime
    created_at = DateTimeField(required=True)  # TODO is this DateTime
