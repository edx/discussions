"""
Discussions Interface
"""

from discussions.api.v1.serializers import ContentsSerializer


def create_thread(request, thread_data):
    the_data = {
        "commentable_id": thread_data.get("commentable_id"),
        "course_id":thread_data.get("course_id"),
        "title": thread_data.get("title"),
        "body": thread_data.get("body"),
        "_type": thread_data.get("type")
        }
    # if thread_data["group_id"]:
    #     data["group_id"] = thread_data["group_id"]

    user = request.user
    serializer = ContentsSerializer(data={})
    if not serializer.is_valid():
        return None
    serializer.save()
    api_thread = serializer.data

    # TODO flag, anon, anon to peers,

    return api_thread
