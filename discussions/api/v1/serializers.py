from discussions.models import User
from rest_framework_mongoengine.serializers import EmbeddedDocumentSerializer


class ReadStatesSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = User.ReadState


class UserSerializer(EmbeddedDocumentSerializer):
    read_states = ReadStatesSerializer(many=True)

    class Meta:
        model = User
