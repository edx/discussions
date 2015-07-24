from rest_framework import generics
from rest_framework.response import Response

from discussions.api.v1.serializers import (
    ContentsSerializer,
    UserSerializer,
    SubscriptionsSerializer
)
from discussions.models import (
    Contents,
    User,
    Subscriptions
)


class UserDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows users to be viewed.
    """
    serializer_class = UserSerializer
    queryset = User.objects
    lookup_field = 'external_id'

    # shouldn't be necessary in theory but DRF is returning Not Found otherwise
    def get_object(self):
        return User.objects.get(external_id=self.kwargs['external_id'])


class ContentsDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows users to be viewed.
    """
    serializer_class = ContentsSerializer
    queryset = Contents.objects
    lookup_field = '_id'

    # shouldn't be necessary in theory but DRF is returning Not Found otherwise
    def get_object(self):
        return Contents.objects.get(_id=str(self.kwargs['_id']))


class SubscriptionsDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows users to be viewed.
    """
    serializer_class = SubscriptionsSerializer
    queryset = Subscriptions.objects
    lookup_field = '_id'

    # shouldn't be necessary in theory but DRF is returning Not Found otherwise
    def get_object(self):
        return Subscriptions.objects.get(_id=str(self.kwargs['_id']))


class TopicsDetailView(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed.
    """
    serializer_class = ContentsSerializer
    queryset = Contents.objects
    lookup_field = 'topic_id'

    def get(self, request, topic_id):
        # TODO Case when topic id is missing? Currently returns 200
        responses = Contents.objects.filter(commentable_id=str(self.kwargs['topic_id']))
        return Response([ContentsSerializer(response).data for response in responses])

