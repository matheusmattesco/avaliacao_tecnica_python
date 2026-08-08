from django.urls import path

from .views import AccessRequestListCreateView


urlpatterns = [
    path(
        "",
        AccessRequestListCreateView.as_view(),
        name="access-request-list-create",
    ),
]