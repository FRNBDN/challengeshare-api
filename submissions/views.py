from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Submission
from .serializers import SubmissionSerializer
from challenge_api.permissions import IsOwnerOrReadOnly

QUERYSET = Submission.objects.annotate(
        reviews=Count(
            'review', distinct=True
        )
    )


class SubmissionList(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = QUERYSET
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'challenge',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = QUERYSET
