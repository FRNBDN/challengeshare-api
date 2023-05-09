from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from challenge_api.permissions import IsOwnerOrReadOnly
from .models import Upload
from cloudinary import uploader, utils
from .serializers import UploadSerializer
from cloudinary.forms import CloudinaryJsFileField


class UploadList(generics.ListCreateAPIView):
    """
    UploadList with added filter for filtering
    Uploads by submission
    """
    serializer_class = UploadSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Upload.objects.all()
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'submission',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UploadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
