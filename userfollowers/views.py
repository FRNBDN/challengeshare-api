from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from challenge_api.permissions import IsOwnerOrReadOnly
from .models import UserFollower
from .serializers import UserFollowerSerializer


class UserFollowerList(generics.ListCreateAPIView):
    serializer_class = UserFollowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = UserFollower.objects.all()

    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'ufollowing__profile',
        'ufollowed__profile'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserFollowerDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = UserFollowerSerializer
    queryset = UserFollower.objects.all()
