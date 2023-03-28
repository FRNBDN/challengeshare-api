from django.contrib.auth.models import User
from .models import Upload
from submissions.models import Submission
from challenges.models import Challenge
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile


class UploadsListViewTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='pw')
        chall = Challenge.objects.create(owner=user, title='test title')
        Submission.objects.create(owner=user, challenge=chall, text='test')

    def test_can_list_uploads(self):
        user = User.objects.get(username='test')
        sub = Submission.objects.get(owner=user)
        Upload.objects.create(owner=user, submission=sub)
        response = self.client.get('/uploads/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_uploads_for_own_submission(self):
        self.client.login(username='test', password='pw')
        response = self.client.post('/uploads/', {
            'owner': '1',
            'submission': '1',
            })
        count = Upload.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_in_user_cant_create_uploads_for_other_user_sub(self):
        self.client.login(username='test2', password='pw')
        response = self.client.post('/uploads/', {
            'owner': '1',
            'submission': '1',
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_logged_in_user_cant_create_uploads(self):
        response = self.client.post('/uploads/', {
            'owner': '1',
            'submission': '1',
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
class UploadsDetailViewTests(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='test', password='pw')
        user2 = User.objects.create_user(username='test2', password='pw')
        chall = Challenge.objects.create(owner=user1, title='test title',
                                         tags=['test',])
        sub = Submission.objects.create(owner=user1,
                                        challenge=chall, text='test')
        Upload.objects.create(owner=user1, submission=sub)

    def test_can_retrieve_upload_using_valid_id(self):
        response = self.client.get('/uploads/1')
        self.assertEqual(response.data['owner'], 'test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_upload_using_invalid_id(self):
        response = self.client.get('/uploads/44')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_user_can_delete_own_uploads(self):
        self.client.login(username='test', password='pw')
        response = self.client.delete('/uploads/1')
        count = Upload.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_other_users_uploads(self):
        self.client.login(username='test2', password='pw')
        response = self.client.delete('/uploads/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)