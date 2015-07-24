from django.http import Http404
from rest_framework import generics
from rest_framework.request import clone_request

from rest_framework.response import Response

from discussions.models import CommentThread, User
from discussions.api.v1.serializers import PaginatedThreadSerializer, UserSerializer


class UserDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    """
    API endpoint that allows users to be viewed.
    """
    serializer_class = UserSerializer

    def get_object(self):
        try:
            return User.objects.get(external_id=self.kwargs['user_id'])
        except User.DoesNotExist:
            raise Http404

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        extra_kwargs = {}
        try:
            instance = self.get_object()
        except Http404:
            # this is derived from https://gist.github.com/tomchristie/a2ace4577eff2c603b1b
            # and supports PUT as create.
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
                instance = None
                extra_kwargs.update({
                    "id": kwargs['user_id'],
                    "external_id": kwargs['user_id'],
                })
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(**extra_kwargs)
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
