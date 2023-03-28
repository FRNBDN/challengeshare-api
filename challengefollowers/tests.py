from django.contrib.auth.models import User
from .models import ChallengeFollower
from challenges.models import Challenge
from rest_framework import status
from rest_framework.test import APITestCase


class ChallengeFollowerListViewTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='pw')
        Challenge.objects.create(owner=user, title='test title')

    def test_can_list_challengefollowers(self):
        user = User.objects.get(username='test')
        challenge = Challenge.objects.get(owner=user)
        ChallengeFollower.objects.create(owner=user, challenge=challenge)
        response = self.client.get('/cfollowers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_loggedn_in_user_can_create_challengefollower(self):
        self.client.login(username='test', password='pw')
        response = self.client.post('/cfollowers/', {
            'owner': '1',
            'challenge': '1'})
        count = ChallengeFollower.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_challengefollower(self):
        response = self.client.post('/cfollowers/', {
            'owner': '1',
            'challenge': '1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ChallengeFollowerDetailViewTests(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='test', password='pw')
        user2 = User.objects.create_user(username='test2', password='pw')
        chall = Challenge.objects.create(owner=user1, title='test title',
                                         tags=['test',])
        ChallengeFollower.objects.create(owner=user1, challenge=chall)

    def test_can_retrieve_challengefollower_using_valid_id(self):
        response = self.client.get('/cfollowers/1')
        self.assertEqual(response.data['challenge'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_challengefollower_using_invalid_id(self):
        response = self.client.get('/cfollowers/300')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_delete_own_challengefollower(self):
        self.client.login(username='test', password='pw')
        response = self.client.delete('/cfollowers/1')
        count = ChallengeFollower.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_other_users_challengefollower(self):
        self.client.login(username='test2', password='pw')
        response = self.client.delete('/cfollowers/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
