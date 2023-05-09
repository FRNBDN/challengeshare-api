from rest_framework import serializers
from criteria.models import Criteria


class CriteriaSerializer(serializers.ModelSerializer):
    """
    Checks to ensure that you are the owner, for deletion
    That you only add criteria to owned dares.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def validate(self, data):
        challenge_owner = data['challenge'].owner
        if self.context['request'].user != challenge_owner:
            raise serializers.ValidationError(
                'You can only add criterias to owned challenges.',
            )
        return data

    class Meta:
        model = Criteria
        fields = [
            'id', 'owner', 'is_owner', 'challenge', 'text',
            'created_at', 'updated_at',
        ]
