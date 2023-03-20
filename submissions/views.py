from rest_framework import generics, permissions
from .models import Submission
from .serializers import SubmissionSerializer
from challenge_api.permissions import IsOwnerOrReadOnly

QUERYSET = Submission.objects.all()


class SubmissionList(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = QUERYSET

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = QUERYSET
