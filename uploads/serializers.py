from rest_framework import serializers
from .models import Upload
from submissions.models import Submission


class UploadSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

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
