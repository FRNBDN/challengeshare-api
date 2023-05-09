from rest_framework import serializers
from .models import Profile
from userfollowers.models import UserFollower


class ProfileSerializer(serializers.ModelSerializer):
    """
    Add fields for challenge, submission interactions
    and checks if owner, followers/ing count
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    submissions_interactions = serializers.ReadOnlyField()
    challenges_interactions = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = UserFollower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'bio', 'image', 'is_owner', 'following_id', 'followers_count',
            'following_count', 'submissions_interactions',
            'challenges_interactions'
        ]
