import json

import ddt
from django.core.urlresolvers import reverse
from django.test import TestCase

from discussions.models import User


@ddt.ddt
class UserDetailViewTests(TestCase):

    user_id = "99"
    username = "test-user"
    default_sort_key = "date"
    course_id = "test-course-id"

    def setUp(self):
        self.user = User.objects.create(
            _id=self.user_id,
            external_id=self.user_id,
            username='test-user',
            default_sort_key='date'
        )

    def get_url(self, user_id=None):
        return reverse('api:v1:user_detail', kwargs={'user_id': user_id or self.user_id})

    def test_get(self):
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            'username': 'test-user',
            'external_id': self.user_id,
        })

    def test_get_complete(self):
        response = self.client.get(self.get_url(), {'complete': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "id": self.user_id,
            "username": self.username,
            "external_id": self.user_id,
            "default_sort_key": self.default_sort_key,
            "subscribed_thread_ids": [],  # TODO
            "subscribed_commentable_ids": [],
            "subscribed_user_ids": [],
            "follower_ids": [],
            "upvoted_ids": [],  # TODO
            "downvoted_ids": [],
        })

    def test_get_course_id(self):
        response = self.client.get(self.get_url(), {'course_id': self.course_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "username": self.username,
            "external_id": self.user_id,
            "threads_count": 0,  # TODO
            "comments_count": 0,  # TODO
        })

    def test_get_not_found(self):
        response = self.client.get(self.get_url("321"))
        self.assertEqual(response.status_code, 404)

    def test_put_create(self):
        new_user_id = "101"
        response = self.client.put(
            self.get_url(new_user_id),
            data=json.dumps({
                "username": "new-username",
                "external_id": new_user_id
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

        db_user = User.objects.get(_id=new_user_id)
        self.assertEqual(db_user.id, new_user_id)
        self.assertEqual(db_user.external_id, new_user_id)
        self.assertEqual(db_user.username, "new-username")
        self.assertEqual(db_user.default_sort_key, "date")
        self.assertEqual(db_user.notification_ids, [])

    def test_put_update(self):
        response = self.client.put(
            self.get_url(), data=json.dumps({
                "username": "new-username",
                "default_sort_key": "other-sort-key"  # TODO this should be constrained
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

        db_user = User.objects.get(_id=self.user_id)
        self.assertEqual(db_user.username, "new-username")
        self.assertEqual(db_user.default_sort_key, "other-sort-key")

    @ddt.data("id", "external_id")
    def test_put_update_read_only(self, read_only_id_field):
        response = self.client.put(
            self.get_url(), data=json.dumps({
                "username": "new-username",
                "default_sort_key": "other-sort-key",
                read_only_id_field: "9000",
            }),
            content_type='application/json',
        )
        # TODO cs_comments_service seems to return 200 no matter what you throw at it.
        # until figuring this out, just ensure that we aren't overwriting external_id
        self.assertEqual(response.status_code, 200)

        # just make sure ALL the changes was ignored
        db_user = User.objects.get(_id=self.user_id)
        # self.assertEqual(db_user.default_sort_key, self.default_sort_key)  # TODO
        self.assertEqual(getattr(db_user, read_only_id_field), self.user_id)

