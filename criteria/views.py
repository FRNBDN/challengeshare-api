from rest_framework import generics, permissions
from challenge_api.permissions import IsOwnerOrReadOnly
from .models import Criteria
from .serializers import CriteriaSerializer


class CriteriaList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CriteriaDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Criteria.objects.all()
    serializer_class = CriteriaSerializer
