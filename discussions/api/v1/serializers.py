from discussions.models import CommentThread, Content, Subscription, User
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from rest_framework import fields, serializers
from rest_framework.pagination import BasePaginationSerializer


class ReadStatesSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = User.ReadState


class UserSerializer(DocumentSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'external_id', 'default_sort_key')
        read_only_fields = ('_id', 'external_id')  # external_id is write-once and should always be synced to _id
        # TODO: actually allowing 'username' to be updated would break other parts of the service so it should
        # be in read-only fields; however, the cs_comments_service implementation actually allows this.

    def to_representation(self, obj):
        obj = super(UserSerializer, self).to_representation(obj)
        if 'request' in self.context:
            if 'complete' in self.context['request'].GET:
                obj.update({
                    "subscribed_thread_ids": [],  # TODO
                    "subscribed_commentable_ids": [],  # ignored
                    "subscribed_user_ids": [],  # ignored
                    "follower_ids": [],  # ignored
                    "upvoted_ids": [],  # TODO
                    "downvoted_ids": [],  # ignored
                })
            else:
                del obj["id"]
                del obj["default_sort_key"]
            if 'course_id' in self.context['request'].GET:
                obj.update({
                    "threads_count": 0,  # TODO
                    "comments_count": 0  # TODO
                })
            return obj


class VoteSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Content.Votes
        fields = ('count', 'down_count', 'point', 'up_count')


class ThreadSerializer(DocumentSerializer):

    votes = VoteSerializer()
    comments_count = fields.IntegerField(source='comment_count')
    user_id = fields.CharField(source='author_id')
    username = fields.CharField(source='author_username')
    endorsed = fields.SerializerMethodField()
    pinned = fields.SerializerMethodField()
    tags = fields.SerializerMethodField()
    type = fields.SerializerMethodField()

    class Meta:
        model = CommentThread
        fields = (
            'abuse_flaggers',
            'anonymous',
            'anonymous_to_peers',
            'at_position_list',
            'body',
            'closed',
            'commentable_id',
            'comments_count',
            'course_id',
            'created_at',
            'endorsed',
            'group_id',
            'id',
            'pinned',
            'tags',
            'thread_type',
            'title',
            'type',
            'updated_at',
            'user_id',
            'username',
            'votes',
        )

    def to_representation(self, obj):
        obj = super(ThreadSerializer, self).to_representation(obj)
        obj["read"] = False  # TODO
        obj["unread_comments_count"] = 0  # TODO
        return obj

    def get_tags(self, instance):
        return []  # this isn't used, so not worth implementing true serialization for.

    def get_type(self, instance):
        return 'thread'

    def get_endorsed(self, instance):
        return getattr(instance, 'endorsed', None) or False  # field may be missing from documents in Mongo

    def get_pinned(self, instance):
        return getattr(instance, 'pinned', None) or False  # field may be missing from documents in Mongo


class CurrentPageField(serializers.Field):
    def to_representation(self, value):
        return value.number


class NumPagesField(serializers.Field):
    def to_representation(self, value):
        return value.paginator.num_pages


class PaginatedThreadSerializer(BasePaginationSerializer):
    results_field = 'collection'
    page = CurrentPageField(source='*')
    num_pages = NumPagesField(source='*')

    class Meta(object):
        object_serializer_class = ThreadSerializer
