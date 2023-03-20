from django.db.models import Count, Q
from rest_framework import generics, permissions, filters
from .models import Challenge
from .serializers import ChallengeSerializer
from challenge_api.permissions import IsOwnerOrReadOnly

QUERYSET = Challenge.objects.all()


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
