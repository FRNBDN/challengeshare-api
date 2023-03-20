from rest_framework import serializers
from criteria.models import Criteria


class CriteriaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Criteria
        fields = [
            'id', 'owner', 'is_owner', 'challenge', 'text',
            'created_at', 'updated_at',
        ]
