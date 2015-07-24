from rest_framework_mongoengine.serializers import EmbeddedDocumentSerializer

from discussions.models import Subscription, User


class ReadStatesSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = User.ReadState


class UserSerializer(EmbeddedDocumentSerializer):
    read_states = ReadStatesSerializer(many=True)

    class Meta:
        model = User
