from rest_framework import generics, permissions
from challenge_api.permissions import IsOwnerOrReadOnly
from .models import Criteria
from .serializers import CriteriaSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CriteriaList(generics.ListCreateAPIView):
    """
    CriteriaList View
    Adds filter for challenges
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer

    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'challenge'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CriteriaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View if not owner, +edit, delete if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer
