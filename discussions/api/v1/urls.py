from django.conf.urls import url, patterns
from discussions.api.v1 import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = patterns('',
    url(
        r'^users/(?P<external_id>\d+)$',
        views.UserDetailView.as_view(),
        name='retrieve_user'
    ),
    url(
        r'^content/(?P<_id>\w+)$',
        views.ContentsDetailView.as_view(),
        name='retrieve_content'
    ),
    url(
        r'^subscriptions/(?P<_id>\w+)$', # TODO Look up our REST conventions
        views.SubscriptionsDetailView.as_view(),
        name='retrieve_subscription'
    ),
)
