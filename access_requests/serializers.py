from rest_framework import serializers

from .models import AccessRequest


class AccessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRequest
        fields = [
            "id",
            "requester_name",
            "requester_email",
            "system",
            "profile",
            "justification",
            "status",
            "decision_reason",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "decision_reason",
            "created_at",
            "updated_at",
        ]