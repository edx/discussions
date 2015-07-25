from django.http import Http404
from mongoengine.queryset import Q
from rest_framework import filters, generics
from rest_framework.request import clone_request
from rest_framework.response import Response

from discussions.api.v1.serializers import PaginatedThreadSerializer, UserSerializer, ThreadSerializer
from discussions.models import CommentThread, User


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
        return Response(serializer.data)


class ThreadQueryFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        """
        Return a filtered queryset.
        """
        # handle course_id
        queryset = queryset.filter(course_id=request.GET['course_id'])

        # handle commentable_ids
        commentable_ids = request.GET.get('commentable_ids', '')
        if commentable_ids:
            queryset = queryset.filter(commentable_id__in=commentable_ids.split(','))

        # handle group_id / group_ids
        group_id_values = [request.GET[k].strip() for k in ('group_id', 'group_ids') if k in request.GET]
        # TODO: if both group_id and group_ids are sent, Bad Request
        assert len(group_id_values) < 2, "cannot pass both group_id and group_ids"
        if group_id_values:
            group_ids = group_id_values[0].split(',')
            q_no_group_id = Q(group_id__not__exists=True)
            q_match_group_id = Q(group_id=group_ids[0]) if len(group_ids) == 1 else Q(group_id__in=group_ids)
            queryset = queryset.filter(q_match_group_id | q_no_group_id)

        # TODO handle flagged
        # TODO handle unread
        # TODO handle unanswered

        return queryset


class ThreadSortFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        """
        Return a filtered queryset.
        """
        sort_key = {
            "activity": "last_activity_at",
            "votes": "votes.point",
            "comments": "comment_count",
        }.get(
            request.GET.get("sort_key"),
            "created_at"
        )

        sort_order = "" if request.GET.get("sort_order") == "asc" else "-"

        order_by = ["-pinned", sort_order + sort_key]
        if sort_key not in ("last_activity_at", "created_at"):
            order_by.append("-created_at")

        return queryset.order_by(*order_by)


class ThreadListView(generics.ListAPIView):
    """
    API endpoint that allows threads to be viewed.
    """
    # TODO re-implement pagination correctly, using non-deprecated APIs.
    # see http://www.django-rest-framework.org/api-guide/pagination/
    paginate_by = 20  # should come from request
    paginate_by_param = 'per_page'
    pagination_serializer_class = PaginatedThreadSerializer

    queryset = CommentThread.objects
    filter_backends = (ThreadQueryFilterBackend, ThreadSortFilterBackend, )
    serializer_class = ThreadSerializer
