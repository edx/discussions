from discussions.models import User
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

from discussions.models import Subscription, User


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
