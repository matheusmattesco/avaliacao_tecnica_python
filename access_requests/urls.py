from django.urls import path

from .views import (
    AccessRequestDecisionView,
    AccessRequestHistoryView,
    AccessRequestListCreateView,
)

urlpatterns = [
    path(
        "",
        AccessRequestListCreateView.as_view(),
        name="access-request-list-create",
    ),
    path(
        "<int:pk>/history/",
        AccessRequestHistoryView.as_view(),
        name="access-request-history",
    ),
    path(
        "<int:pk>/<str:action>/",
        AccessRequestDecisionView.as_view(),
        name="access-request-decision",
    ),
]