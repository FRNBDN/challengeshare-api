from rest_framework import generics, permissions
from challenge_api.permissions import IsOwnerOrReadOnly
from .models import Criteria
from .serializers import CriteriaSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CriteriaList(generics.ListCreateAPIView):
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
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer
