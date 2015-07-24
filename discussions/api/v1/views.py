from rest_framework import generics

from discussions.models import User, Contents
from discussions.api.v1.serializers import (
    UserSerializer,
    ContentsSerializer
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

