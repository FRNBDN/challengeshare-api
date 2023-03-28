from django.contrib.auth.models import User
from .models import Review
from submissions.models import Submission
from challenges.models import Challenge
from rest_framework import status
from rest_framework.test import APITestCase


class ProfileListView(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='pw')
        chall = Challenge.objects.create(owner=user, title='test title')
        Submission.objects.create(owner=user, challenge=chall)

    def test_can_list_reviews(self):
        user = User.objects.get(username='test')
        sub = Submission.objects.get(owner=user)
        Review.objects.create(owner=user, submission=sub, vote_pass=False)
        response = self.client.get('/reviews/')
        count = Review.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_review(self):
        self.client.login(username='test', password='pw')
        response = self.client.post('/reviews/', {
            'body': 'test body',
            'vote_pass': 'False',
            'submission': '1'})
        count = Review.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_logged_in_user_cant_create_multiple_review(self):
        user = User.objects.get(username='test')
        sub = Submission.objects.get(owner=user)
        Review.objects.create(owner=user, submission=sub, vote_pass=False, 
                              body='test')
        self.client.login(username='test', password='pw')
        response = self.client.post('/reviews/', {
            'body': 'secondreview',
            'vote_pass': 'False',
            'submission': '1'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_logged_in_user_cant_create_review(self):
        response = self.client.post('/reviews/', {
            'body': 'test body',
            'vote_pass': 'False',
            'submission': '1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewDetailViewTests(APITestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='test', password='pw')
        user2 = User.objects.create_user(username='test2', password='pw')
        chall = Challenge.objects.create(owner=user1, title='test title')
        sub = Submission.objects.create(owner=user1, challenge=chall)
        Review.objects.create(owner=user1, submission=sub, vote_pass=False)

    def test_can_retrieve_review_using_valid_id(self):
        response = self.client.get('/reviews/1')
        self.assertEqual(response.data['vote_pass'], False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_review_using_invalid_id(self):
        response = self.client.get('/reviews/1222')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_review(self):
        self.client.login(username='test', password='pw')
        response = self.client.put('/reviews/1', {'body': 'test body'})
        review = Review.objects.filter(pk=1).first()
        self.assertEqual(review.body, 'test body')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_other_users_review(self):
        self.client.login(username='test2', password='pw')
        response = self.client.put('/reviews/1', {'body': 'test body'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_review(self):
        self.client.login(username='test', password='pw')
        response = self.client.delete('/reviews/1')
        count = Review.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_other_users_reviews(self):
        self.client.login(username='test2', password='pw')
        response = self.client.delete('/reviews/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

