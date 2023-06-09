from django.db import IntegrityError
from rest_framework import serializers
from .models import UserFollower


class UserFollowerSerializer(serializers.ModelSerializer):
    """
    add fields for owner and followed name to be less confusing
    validates so you dont follow yourself
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')
    owner_id = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = UserFollower
        fields = [
            'id', 'owner', 'owner_id', 'created_at', 'followed',
            'followed_name'
        ]

    def create(self, validated_data):
        followed = validated_data['followed']
        if followed == self.context['request'].user:
            raise serializers.ValidationError({
                'detail': 'You cannot follow yourself'
            })
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})
