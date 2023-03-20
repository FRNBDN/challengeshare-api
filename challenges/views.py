from django.db.models import Count, Q
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Challenge
from .serializers import ChallengeSerializer
from challenge_api.permissions import IsOwnerOrReadOnly

QUERYSET = Challenge.objects.annotate(
     users_count=Count('challengefollower', distinct=True),
     submissions_count=Count('submission', distinct=True),
     completed_count=Count(
        'submission', filter=Q(submission__status=2)
        )
    ).order_by('-created_at')


class ChallengesList(generics.ListCreateAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = QUERYSET

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = QUERYSET
