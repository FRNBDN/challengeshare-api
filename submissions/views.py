from django.db.models import Count
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Submission
from .serializers import SubmissionSerializer
from challenge_api.permissions import IsOwnerOrReadOnly

QUERYSET = Submission.objects.annotate(
        reviews=Count(
            'review', distinct=True
        ),
    ).order_by('-created_at')


class SubmissionList(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = QUERYSET
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        'challenge',
        'owner__ufollowed__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'text',
    ]

    ordering_fields = [
        'status',
        'reviews',
        'completed_count',
        'created_at',
        'updated_at'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = QUERYSET
