from django.contrib.auth.models import User
from .models import Challenge
from rest_framework import status
from rest_framework.test import APITestCase


class ChallengeListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='pw')

    def test_can_list_challenges(self):
        user = User.objects.get(username='test')
        Challenge.objects.create(owner=user, title='test title')
        response = self.client.get('/challenges/')
        count = Challenge.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_challenge(self):
        self.client.login(username='test', password='pw')
        response = self.client.post('/challenges/', {
            'title': 'test title',})
        count = Challenge.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_challenge(self):
        response = self.client.post('/challenges/', {
            'title': 'test title',})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ChallengeDetailViewTests(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='test', password='pw')
        user2 = User.objects.create_user(username='test2', password='pw')
        Challenge.objects.create(owner=user1, title='test title',)
        Challenge.objects.create(owner=user2, title='test title2',)

    def test_can_retrieve_challenge_using_valid_id(self):
        response = self.client.get('/challenges/1')
        self.assertEqual(response.data['title'], 'test title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_challenge_using_invalid_id(self):
        response = self.client.get('/challenges/300')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_challenge(self):
        self.client.login(username='test', password='pw')
        response = self.client.put('/challenges/1', {'title': 'updated title',
                                                     'tags': ['test',]})
        challenge = Challenge.objects.filter(pk=1).first()
        self.assertEqual(challenge.title, 'updated title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_other_users_challenges(self):
        self.client.login(username='test', password='pw')
        response = self.client.put('/challenges/2', {'title': 'updated title',
                                                     'tags': ['test',]})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_challenge(self):
        self.client.login(username='test', password='pw')
        response = self.client.delete('/challenges/1')
        count = Challenge.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_other_users_challenges(self):
        self.client.login(username='test', password='pw')
        response = self.client.delete('/challenges/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
