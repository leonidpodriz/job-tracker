import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from applications.models import Application
from applications.views import ApplicationViewSet

APPLICATIONS_V1_URI = "/api/v1/applications/"


@pytest.fixture
def application(user):
    return Application.objects.create(user=user)


@pytest.fixture
def application_method_requests(application, client):
    return [
        (client.get, reverse("applications:applications-list")),
        (client.post, reverse("applications:applications-list")),
        (client.get, reverse("applications:applications-detail", args=[application.id])),
        (client.put, reverse("applications:applications-detail", args=[application.id])),
        (client.patch, reverse("applications:applications-detail", args=[application.id])),
        (client.delete, reverse("applications:applications-detail", args=[application.id])),
    ]


@pytest.mark.django_db
def test_unauthorized_requests(user, application_method_requests):
    for method, uri in application_method_requests:
        response = method(uri)

        assert (
                response.status_code == status.HTTP_401_UNAUTHORIZED
        ), "Expected Response Code 401, received {0} instead. (Method: {1})".format(
            response.status_code, method.__name__
        )


def test_applications_operations_without_permissions(user, client, application_method_requests):
    client.force_login(user)

    for method, uri in application_method_requests:
        response = method(uri)

        assert (
                response.status_code == status.HTTP_403_FORBIDDEN
        ), "Expected Response Code 403, received {0} instead. (Method: {1})".format(
            response.status_code, method
        )


def test_applications_create(admin_user):
    factory = APIRequestFactory()
    view = ApplicationViewSet.as_view(
        {
            "post": "create",
        }
    )

    request = factory.post(APPLICATIONS_V1_URI, {}, format="json")
    force_authenticate(request, user=admin_user)
    response = view(request)

    assert (
            response.status_code == status.HTTP_201_CREATED
    ), "Expected Response Code 201, received {0} instead.".format(
        response.status_code,
    )

    assert "id" in response.data, "Response data does not contain `id` field."

    assert (
            response.data.get("status") == "pending"
    ), "Response data does not contain `status` field with value `pending`."

    assert (
            response.data.get("user", {}).get("id") == admin_user.id
    ), "Response data does not contain `user` field with correct `id`."

    required_user_fields = {"username", "first_name", "last_name", "email", "is_active"}
    response_user = response.data.get("user", {})
    insufficient_fields = required_user_fields - set(response_user.keys())

    assert (
        not insufficient_fields
    ), "Response data does not contain `user` field with required fields: {0}".format(
        ", ".join(insufficient_fields)
    )


status_cases = (
    {
        "value": "accepted",
        "is_valid": True,
    },
    {
        "value": "rejected",
        "is_valid": True,
    },
    {
        "value": "pending",
        "is_valid": True,
    },
    {
        "value": "invalid",
        "is_valid": False,
    },
    {
        "value": "some_random_status",
        "is_valid": False,
    },
)


@pytest.mark.parametrize("status_case", status_cases)
def test_applications_status_change(admin_user, status_case):
    application = Application.objects.create(user=admin_user)
    factory = APIRequestFactory()
    view = ApplicationViewSet.as_view(
        {
            "patch": "partial_update",
        }
    )

    application_status = status_case["value"]
    is_valid_expected = status_case["is_valid"]

    request = factory.patch(
        APPLICATIONS_V1_URI + "{0}/".format(application.id),
        {"status": application_status},
        format="json",
    )
    force_authenticate(request, user=admin_user)
    response = view(request, pk=application.id)

    if is_valid_expected:
        assert (
                response.status_code == status.HTTP_200_OK
        ), "Expected Response Code 200, received {0} instead. (Status: {1})".format(
            response.status_code,
            application_status,
        )

        assert (
                response.data.get("status") == application_status
        ), "Response data does not contain `status` field with value `{0}`.".format(
            application_status,
        )
    else:
        assert (
                response.status_code == status.HTTP_400_BAD_REQUEST
        ), "Expected Response Code 400, received {0} instead. (Status: {1})".format(
            response.status_code,
            application_status,
        )


notes_cases = (
    "some notes",
    "some other notes",
    "some other notes 123",
    "some other notes 123 456",
    "note with special characters: !@#$%^&*()_+{}[]|\\:;\"'<>,.?/",
    None,
)


@pytest.mark.parametrize("notes", notes_cases)
def test_applications_notes(admin_user, notes):
    application = Application.objects.create(user=admin_user)
    factory = APIRequestFactory()
    view = ApplicationViewSet.as_view(
        {
            "patch": "partial_update",
        }
    )

    request = factory.patch(
        APPLICATIONS_V1_URI + "{0}/".format(application.id),
        {"notes": notes},
        format="json",
    )
    force_authenticate(request, user=admin_user)
    response = view(request, pk=application.id)

    assert (
            response.status_code == status.HTTP_200_OK
    ), "Expected Response Code 200, received {0} instead.".format(
        response.status_code,
    )

    assert (
            response.data.get("notes") == notes
    ), "Response data does not contain `notes` field with value `some notes`."


def test_applications_list(admin_user):
    factory = APIRequestFactory()
    view = ApplicationViewSet.as_view(
        {
            "get": "list",
        }
    )

    request = factory.get(APPLICATIONS_V1_URI)
    force_authenticate(request, user=admin_user)
    response = view(request)

    assert (
            response.status_code == status.HTTP_200_OK
    ), "Expected Response Code 200, received {0} instead.".format(
        response.status_code,
    )
