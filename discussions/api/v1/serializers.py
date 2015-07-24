from discussions.models import CommentThread, Content, User
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from rest_framework.pagination import PaginationSerializer


class ReadStatesSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = User.ReadState


class UserSerializer(DocumentSerializer):
    read_states = ReadStatesSerializer(many=True)

    class Meta:
        model = User


class VoteSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Content.Votes


class ThreadSerializer(DocumentSerializer):
    votes = VoteSerializer()

    class Meta:
        model = CommentThread


class PaginatedThreadSerializer(PaginationSerializer):
    class Meta(object):
        object_serializer_class = ThreadSerializer
