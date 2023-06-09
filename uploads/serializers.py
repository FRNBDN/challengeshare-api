from rest_framework import serializers
from .models import Upload
from submissions.models import Submission


class UploadSerializer(serializers.ModelSerializer):
    """
    Serializer validates size of the image and if
    user is uploading to owned submissions.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def validate_upload(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value

    def validate(self, data):
        submission_owner = data['submission'].owner
        if self.context['request'].user != submission_owner:
            raise serializers.ValidationError(
                'You can only add uploads to owned submissions.',
            )
        return data

    class Meta:
        model = Upload
        fields = [
            'id', 'owner', 'is_owner', 'submission', 'created_at', 'upload'
        ]
