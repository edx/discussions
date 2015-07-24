from django.conf.urls import url, patterns
from discussions.api.v1 import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = patterns(
    '',
    url(
        r'^users/(?P<user_id>\d+)$',
        views.UserDetailView.as_view(),
        name='user_detail'
    ),
    url(
        r'^threads/$',
        views.ThreadListView.as_view(),
        name='threads'
    )
)
