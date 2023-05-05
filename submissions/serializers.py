from rest_framework import serializers
from .models import Submission
from uploads.models import Upload
from reviews.models import Review
from django.db import IntegrityError


class SubmissionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    reviews = serializers.ReadOnlyField()
    uploads = serializers.SerializerMethodField()
    has_reviewed = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

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

    def get_has_reviewed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            review = Review.objects.filter(
                owner=user, submission=obj
            ).first()
            return review is not None
        return False

    def get_status(self, obj):
        vote_pass = Review.objects.filter(
            submission=obj, vote_pass=True).count()
        reviews = Review.objects.filter(submission=obj).count()
        if reviews < 3:
            return 1
        elif vote_pass > reviews:
            return 2
        else:
            return 3

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})

    class Meta:
        model = Submission
        fields = [
            'id', 'owner', 'challenge', 'text', 'is_owner',
            'profile_id', 'profile_image',
            'status', 'reviews', 'uploads', 'created_at',
            'updated_at', 'has_reviewed'
        ]
