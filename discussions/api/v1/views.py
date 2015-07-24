from mongoengine.queryset import Q
from rest_framework import generics, status
from rest_framework.response import Response

from discussions.models import Comment, CommentThread, User
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
        """
        Get threads.

        Parameters:
            Required:
                - course_id
            Others:
                - user_id
                - flagged
                - unread
                - unanswered
                - commentable_ids
                - group_id
                - group_ids
                - sort_key
                - sort_order
                - page
                - per_page
        """
        # Validate the request
        course_id = request.query_params.get('course_id')
        if not course_id:
            # TODO: developer message?
            return Response(status=status.HTTP_400_BAD_REQUEST)

        comment_threads = CommentThread.objects.filter(course_id=course_id)

        # TODO: what are expected values for this parameter?
        if request.query_params.get('flagged') == 'true':
            flagged_comments = Comment.objects.filter(
                course_id=course_id,
                abuse_flaggers__ne=list()
            ).only('comment_thread_id')
            # TODO: do this efficiently
            comment_thread_ids = [comment.comment_thread_id for comment in flagged_comments.only('comment_thread_id')]
            comment_threads = comment_threads.filter(Q(abuse_flaggers__ne=list()) | Q(_id__in=comment_thread_ids))

        # TODO: what are expected values for this parameter?
        if request.query_params.get('unread') == 'true':
            pass

        page = self.paginate_queryset(comment_threads)
        serializer = self.pagination_serializer_class(page)
        return Response(serializer.data)
