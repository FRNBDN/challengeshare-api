from rest_framework import serializers
from .models import Submission
from uploads.models import Upload


class SubmissionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    reviews = serializers.ReadOnlyField()
    uploads = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_uploads(self, obj):
        uploads = Upload.objects.filter(
            submission=obj
        )
        upload_list = []
        for upload in uploads:
            upload_list.append(upload.id)
        return upload_list

    class Meta:
        model = Submission
        fields = [
            'id', 'owner', 'challenge', 'text', 'is_owner',
            'status', 'reviews', 'uploads', 'created_at',
            'updated_at'
        ]
