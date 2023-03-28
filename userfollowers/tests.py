from django.contrib.auth.models import User
from .models import UserFollower
from rest_framework import status
from rest_framework.test import APITestCase


class UserFollowerListViewTests(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='test', password='pw')
        user2 = User.objects.create_user(username='test2', password='pw')
        UserFollower.objects.create(owner=user1, followed=user2)

    def test_can_list_userfollowers(self):
        response = self.client.get('/ufollowers/')
        count = UserFollower.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_loggedn_in_user_can_create_userfollower(self):
        self.client.login(username='test2', password='pw')
        response = self.client.post('/ufollowers/', {
            'owner': '2',
            'followed': '1'})
        count = UserFollower.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_loggedn_in_user_cant_create_multiple_userfollower(self):
        self.client.login(username='test', password='pw')
        response = self.client.post('/ufollowers/', {
            'owner': '1',
            'followed': '2'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_not_logged_in_cant_create_userfollower(self):
        response = self.client.post('/ufollowers/', {
            'owner': '2',
            'followed': '1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ChallengeFollowerDetailViewTests(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='test', password='pw')
        user2 = User.objects.create_user(username='test2', password='pw')
        UserFollower.objects.create(owner=user1, followed=user2)

    def test_can_retrieve_userfollower_using_valid_id(self):
        response = self.client.get('/ufollowers/1')
        self.assertEqual(response.data['followed'], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_userfollower_using_invalid_id(self):
        response = self.client.get('/ufollowers/399')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_delete_own_userfollower(self):
        self.client.login(username='test', password='pw')
        response = self.client.delete('/ufollowers/1')
        count = UserFollower.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_other_users_userfollower(self):
        self.client.login(username='test2', password='pw')
        response = self.client.delete('/ufollowers/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
