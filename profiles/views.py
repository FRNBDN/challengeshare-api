from django.db.models import Count
from rest_framework import generics, filters
from challenge_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer

QUERYSET = Profile.objects.all()


class ProfileList(generics.ListAPIView):
    queryset = QUERYSET
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = QUERYSET
    serializer_class = ProfileSerializer
