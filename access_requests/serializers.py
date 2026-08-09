from rest_framework import serializers

from .models import AccessRequest, DecisionHistory


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

class DecisionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionHistory
        fields = [
            "id",
            "action",
            "reason",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "action",
            "reason",
            "created_at",
        ]