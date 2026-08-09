from django.db import transaction

from .models import AccessRequest, DecisionHistory


class InvalidStatusError(Exception):
    pass


class AccessRequestService:

    @staticmethod
    @transaction.atomic
    def approve(access_request, decision_reason):
        if access_request.status != AccessRequest.Status.PENDING:
            raise InvalidStatusError(
                "Only pending requests can be approved."
            )

        if not decision_reason:
            raise ValueError(
                "Decision reason is required."
            )

        access_request.status = AccessRequest.Status.APPROVED
        access_request.decision_reason = decision_reason
        access_request.save(
            update_fields=[
                "status",
                "decision_reason",
                "updated_at",
            ]
        )

        DecisionHistory.objects.create(
            access_request=access_request,
            action=DecisionHistory.Action.APPROVED,
            reason=decision_reason,
        )

        return access_request


    @staticmethod
    @transaction.atomic
    def reject(access_request, decision_reason):
        if access_request.status != AccessRequest.Status.PENDING:
            raise InvalidStatusError(
                "Only pending requests can be rejected."
            )

        if not decision_reason:
            raise ValueError(
                "Decision reason is required."
            )

        access_request.status = AccessRequest.Status.REJECTED
        access_request.decision_reason = decision_reason
        access_request.save(
            update_fields=[
                "status",
                "decision_reason",
                "updated_at",
            ]
        )

        DecisionHistory.objects.create(
            access_request=access_request,
            action=DecisionHistory.Action.REJECTED,
            reason=decision_reason,
        )

        return access_request
