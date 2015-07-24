from rest_framework import generics
from rest_framework.response import Response

from discussions.models import CommentThread, User
from discussions.api.v1.serializers import PaginatedThreadSerializer, UserSerializer


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


class ThreadListView(generics.ListAPIView):
    """
    API endpoint that allows threads to be viewed.
    """
    paginate_by = 10
    paginate_by_param = 'per_page'
    pagination_serializer_class = PaginatedThreadSerializer

    def get(self, request):
        comment_threads = CommentThread.objects
        page = self.paginate_queryset(comment_threads)
        serializer = self.pagination_serializer_class(page)
        return Response(serializer.data)
