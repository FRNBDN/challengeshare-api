from rest_framework import serializers
from .models import Challenge
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class ChallengeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Challenge
        fields = [
            'id', 'owner', 'title', 'is_owner', 'description',
            'criteria', 'profile_id', 'tags', 
            'profile_image', 'created_at', 'updated_at',
        ]