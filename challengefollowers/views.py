from rest_framework import generics, permissions
from challenge_api.permissions import IsOwnerOrReadOnly
from .models import ChallengeFollower
from .serializers import ChallengeFollowerSerializer


class ChallengeFollowerList(generics.ListCreateAPIView):
    serializer_class = ChallengeFollower
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ChallengeFollower.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ChallengeFollowerDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ChallengeFollowerSerializer
    queryset = ChallengeFollower.objects.all()
