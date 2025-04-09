"""Routes."""

# Django
from django.urls import path

from .views import create_requests, manage_requests

app_name: str = "altcorp"

urlpatterns = [
    path("", create_requests.index_view, name="index"),
    # create_requests
    path(
        "create_requests", create_requests.create_requests, name="create_requests"
    ),  # main requests page
    path(
        "request_corporations",
        create_requests.request_corporations,
        name="request_corporations",
    ),  # requests corporation list
    path(
        "request_corp_join/<int:corporation_id>/",
        create_requests.request_corp_join,
        name="request_corp_join",
    ),  # requests corp standing
    path(
        "remove_corp_join/<int:altcorp_id>/",
        create_requests.remove_corp_join,
        name="remove_corp_join",
    ),  # remove request
    # manage requests
    path("manage/", manage_requests.manage_requests, name="manage"),
    path(
        "manage/requests/",
        manage_requests.requests_list,
        name="manage_requests_list",
    ),  # requests list
    path(
        "manage/revocations/",
        manage_requests.revocations_list,
        name="manage_revocations_list",
    ),  # revocations list
    path(
        "manage/requests/<int:request_id>/",
        manage_requests.manage_requests_write,
        name="manage_requests_write",
    ),  # manage requests write
]
