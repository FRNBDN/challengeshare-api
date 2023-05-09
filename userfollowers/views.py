from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from challenge_api.permissions import IsOwnerOrReadOnly
from .models import UserFollower
from .serializers import UserFollowerSerializer


class UserFollowerList(generics.ListCreateAPIView):
    """
    UserFollower list view with filters for people following
    user and people user is following
    """
    serializer_class = UserFollowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = UserFollower.objects.all()

    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__profile',
        'followed__profile'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserFollowerDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = UserFollowerSerializer
    queryset = UserFollower.objects.all()
