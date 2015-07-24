from rest_framework_mongoengine.serializers import EmbeddedDocumentSerializer

from discussions.models import (
    Contents,
    Subscriptions,
    User,
)


class ReadStatesSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = User.ReadState


class UserSerializer(EmbeddedDocumentSerializer):
    read_states = ReadStatesSerializer(many=True)

    class Meta:
        model = User


class VotesSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Contents.Votes


class ContentsSerializer(EmbeddedDocumentSerializer):
    votes = VotesSerializer()

    class Meta:
        model = Contents


class SubscriptionsSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Subscriptions
