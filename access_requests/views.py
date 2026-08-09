from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AccessRequest, DecisionHistory
from .serializers import (
    AccessRequestSerializer,
    DecisionHistorySerializer,
)
from .services import AccessRequestService, InvalidStatusError

class AccessRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = AccessRequestSerializer

    def get_queryset(self):
        queryset = AccessRequest.objects.all()

        status_filter = self.request.query_params.get("status")
        system_filter = self.request.query_params.get("system")

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if system_filter:
            queryset = queryset.filter(system=system_filter)

        return queryset

class AccessRequestDecisionView(APIView):

    def post(self, request, pk, action):
        try:
            access_request = AccessRequest.objects.get(pk=pk)
        except AccessRequest.DoesNotExist:
            return Response(
                {"detail": "Access request not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        decision_reason = request.data.get("decision_reason")

        try:
            if action == "approve":
                AccessRequestService.approve(
                    access_request,
                    decision_reason,
                )

            elif action == "reject":
                AccessRequestService.reject(
                    access_request,
                    decision_reason,
                )

            else:
                return Response(
                    {"detail": "Invalid action."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except InvalidStatusError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AccessRequestSerializer(access_request)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class AccessRequestHistoryView(generics.ListAPIView):
    serializer_class = DecisionHistorySerializer

    def get_queryset(self):
        return DecisionHistory.objects.filter(
            access_request_id=self.kwargs["pk"]
        ).order_by("-created_at")