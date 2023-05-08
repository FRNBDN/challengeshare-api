from django.contrib.auth.models import User
from .models import Criteria
from challenges.models import Challenge
from rest_framework import status
from rest_framework.test import APITestCase


class CriteriaListViewTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='pw')
        chall = Challenge.objects.create(owner=user, title='test title')

    def test_can_list_criteria(self):
        user = User.objects.get(username='test')
        chall = Challenge.objects.get(owner=user)
        Criteria.objects.create(owner=user, challenge=chall)
        response = self.client.get('/criteria/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_criteria_to_own_challenge(self):
        self.client.login(username='test', password='pw')
        response = self.client.post('/criteria/', {
            'owner': '1',
            'challenge': '1',
            'text': 'text here'})
        count = Criteria.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_in_user_cant_create_criteria_to_other_users_chall(self):
        self.client.login(username='test2', password='pw')
        response = self.client.post('/criteria/', {
            'owner': '1',
            'challenge': '1',
            'text': 'text here'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_logged_in_user_cant_create_criteria(self):
        response = self.client.post('/criteria/', {
            'owner': '1',
            'challenge': '1',
            'text': 'text here'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CriteriaDetailViewTests(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='test', password='pw')
        user2 = User.objects.create_user(username='test2', password='pw')
        chall = Challenge.objects.create(owner=user1, title='test title')
        Criteria.objects.create(owner=user1, challenge=chall, text='test text')

    def test_can_retrieve_criteria_using_valid_id(self):
        response = self.client.get('/criteria/1')
        self.assertEqual(response.data['text'], 'test text')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_criteria_using_invalid_id(self):
        response = self.client.get('/criteria/111')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_delete_own_criteria(self):
        self.client.login(username='test', password='pw')
        response = self.client.delete('/criteria/1')
        count = Criteria.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_other_users_criteria(self):
        self.client.login(username='test2', password='pw')
        response = self.client.delete('/criteria/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
