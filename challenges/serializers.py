from rest_framework import serializers
from .models import Challenge
from criteria.models import Criteria
from submissions.models import Submission
from challengefollowers.models import ChallengeFollower
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class ChallengeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    criteria = serializers.SerializerMethodField()
    users_count = serializers.ReadOnlyField()
    submissions = serializers.SerializerMethodField()
    submissions_count = serializers.ReadOnlyField()
    cfollow_id = serializers.SerializerMethodField()
    completed_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_criteria(self, obj):
        request = self.context['request']
        criteria = Criteria.objects.filter(
            challenge=obj
            )
        criterion_list = []
        for criterion in criteria:
            criterion_list.append(criterion.id)
        return criterion_list

    def get_submissions(self, obj):
        request = self.context['request']
        submissions = Submission.objects.filter(
            challenge=obj
            )
        submissionList = []
        for submission in submissions:
            submissionList.append(submission.id)
        return submissionList

    def get_cfollow_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            cfollow = ChallengeFollower.objects.filter(
                owner=user, challenge=obj
            ).first()
            return cfollow.id if cfollow else None
        return None

    class Meta:
        model = Challenge
        fields = [
            'id', 'owner', 'title', 'is_owner', 'description',
            'category', 'profile_id', 'tags', 'profile_image', 'users_count',
            'created_at', 'updated_at', 'criteria', 'submissions',
            'submissions_count', 'cfollow_id', 'completed_count'
        ]