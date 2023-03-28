from django.contrib.auth.models import User
from .models import Profile
from rest_framework import status
from rest_framework.test import APITestCase


class ProfileListView(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='pw')

    def test_can_list_profiles(self):
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileDetailViewTest(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='test', password='pw')
        user2 = User.objects.create_user(username='test2', password='pw')

    def test_can_retrieve_profile_using_valid_id(self):
        response = self.client.get('/profiles/1')
        self.assertEqual(response.data['owner'], 'test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_profile_using_invalid_id(self):
        response = self.client.get('/profiles/111')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_profile(self):
        self.client.login(username='test', password='pw')
        response = self.client.put('/profiles/1', {'name': 'test'})
        profile = Profile.objects.filter(pk=1).first()
        self.assertEqual(profile.name, 'test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_other_users_profile(self):
        self.client.login(username='test2', password='pw')
        response = self.client.put('/profiles/1', {'name': 'test'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
