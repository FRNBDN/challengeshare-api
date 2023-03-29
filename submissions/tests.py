from django.contrib.auth.models import User
from challenges.models import Challenge
from .models import Submission
from rest_framework import status
from rest_framework.test import APITestCase
import json


class SubmissionListViewTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='pw')
        chall = Challenge.objects.create(owner=user, title='test title')

    def test_can_list_submissions(self):
        user = User.objects.get(username='test')
        chall = Challenge.objects.get(owner=user)
        Submission.objects.create(owner=user, challenge=chall)
        response = self.client.get('/submissions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_submission(self):
        self.client.login(username='test', password='pw')
        response = self.client.post('/submissions/', {
            'text': 'test text',
            'status': '1',
            'challenge': '1'})
        count = Submission.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_in_user_cant_create_multi_submissions_to_same_chall(self):
        user = User.objects.get(username='test')
        chall = Challenge.objects.get(owner=user)
        Submission.objects.create(owner=user, challenge=chall, status=1)
        self.client.login(username='test', password='pw')
        response = self.client.post('/submissions/', {
            'text': 'test text',
            'status': '1',
            'challenge': '1'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def not_test_logged_in_user_cant_create_submission(self):
        self.client.login(username='test', password='pw')
        response = self.client.post('/submissions/', {
            'text': 'test text',
            'status': '1',
            'challenge': '1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubmissionsDetailViewTests(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='test', password='pw')
        user2 = User.objects.create_user(username='test2', password='pw')
        chall = Challenge.objects.create(owner=user1, title='test title')
        Submission.objects.create(owner=user1,
                                  challenge=chall, status=1, text='test text')
        Submission.objects.create(owner=user2,
                                  challenge=chall, status=1, text='test2 text')

    def test_can_retrieve_submission_using_valid_id(self):
        response = self.client.get('/submissions/1')
        self.assertEqual(response.data['text'], 'test text')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_review_using_invalid_id(self):
        response = self.client.get('/submissions/1222')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_submission(self):
        self.client.login(username='test', password='pw')
        response = self.client.put('/submissions/1', {'text': 'updated text',
                                   'challenge': '1'})
        submission = Submission.objects.filter(pk=1).first()
        self.assertEqual(submission.text, 'updated text')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_other_users_submission(self):
        self.client.login(username='test2', password='pw')
        response = self.client.put('/submissions/1', {'text': 'update text'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_submission(self):
        self.client.login(username='test', password='pw')
        response = self.client.delete('/submissions/1')
        count = Submission.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_other_users_submission(self):
        self.client.login(username='test2', password='pw')
        response = self.client.delete('/submissions/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
