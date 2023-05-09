from django.db import IntegrityError
from rest_framework import serializers
from .models import ChallengeFollower


class ChallengeFollowerSerializer(serializers.ModelSerializer):
    """
    CFollowSerializer
    Validates if user is trying to follow own challenge
    or if the user is tryng to follow again.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    challenge_name = serializers.ReadOnlyField(source='challenge.title')

    class Meta:
        model = ChallengeFollower
        fields = [
            'id', 'owner', 'created_at', 'challenge', 'challenge_name'
        ]

    def create(self, validated_data):
        challenge = validated_data['challenge']
        if challenge.owner == self.context['request'].user:
            raise serializers.ValidationError({
                'detail': 'You cannot follow your own challenge'
            })
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})
