from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from challenge_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer

QUERYSET = Profile.objects.annotate(
        followers_count=Count(
            'owner__ufollowed', distinct=True
            ),
        following_count=Count(
            'owner__ufollowing', distinct=True
            ),
        challenges_interactions=Count(
            'owner__challenge__submission__review', distinct=True
        )+Count(
            'owner__challenge__submission', distinct=True
        ),
        submissions_interactions=Count(
            'owner__submission__review', distinct=True
        )+Count(
            'owner__submission', distinct=True
        )
    ).order_by('-created_at')


class ProfileList(generics.ListAPIView):
    queryset = QUERYSET
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__ufollowing__followed__profile',
        'owner__ufollowed__owner__profile'
    ]
    ordering_fields = [
        'ufollowers_count',
        'ufollowing_count',
        'challenges_created',
        'owner__ufollowing__created_at',
        'owner__ufollowed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = QUERYSET
    serializer_class = ProfileSerializer
