from rest_framework import generics, permissions
from challenge_api.permissions import IsOwnerOrReadOnly
from .models import ChallengeFollower
from .serializers import ChallengeFollowerSerializer


class ChallengeFollowerList(generics.ListCreateAPIView):
    """
    List View for ChallengeFollower,
    Lets users view all instances, auth needed
    if create
    """
    serializer_class = ChallengeFollowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ChallengeFollower.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ChallengeFollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Detail view for ChallengeFollower,
    Specific ChallengeFollower, view, delete
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ChallengeFollowerSerializer
    queryset = ChallengeFollower.objects.all()
