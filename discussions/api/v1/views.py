from rest_framework import generics

from discussions.models import User
from discussions.api.v1.serializers import UserSerializer


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
