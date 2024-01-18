from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from applications.views import ApplicationViewSet

APPLICATIONS_V1_URI = '/api/v1/applications/'


def test_unauthorized_requests():
    factory = APIRequestFactory()
    view = ApplicationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })

    requests = [
        factory.get(APPLICATIONS_V1_URI),
        factory.put(APPLICATIONS_V1_URI),
        factory.patch(APPLICATIONS_V1_URI),
        factory.delete(APPLICATIONS_V1_URI)
    ]

    for request in requests:
        response = view(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            'Expected Response Code 401, received {0} instead. (Method: {1})'.format(
                response.status_code,
                request.method
            )
        )


def test_applications_create(user):
    factory = APIRequestFactory()
    view = ApplicationViewSet.as_view({
        'post': 'create',
    })

    request = factory.post(APPLICATIONS_V1_URI, {})
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED, (
        'Expected Response Code 201, received {0} instead.'.format(
            response.status_code,
        )
    )

    assert 'id' in response.data, (
        'Response data does not contain `id` field.'
    )

    assert response.data.get('status') == 'pending', (
        'Response data does not contain `status` field with value `pending`.'
    )

    assert response.data.get('user', {}).get('id') == user.id, (
        'Response data does not contain `user` field with correct `id`.'
    )

    required_user_fields = {'username', 'first_name', 'last_name', 'email', 'is_active'}
    response_user = response.data.get('user', {})
    insufficient_fields = required_user_fields - set(response_user.keys())

    assert not insufficient_fields, (
        'Response data does not contain `user` field with required fields: {0}'.format(
            ', '.join(insufficient_fields)
        )
    )


def test_applications_list(user):
    factory = APIRequestFactory()
    view = ApplicationViewSet.as_view({
        'get': 'list',
    })

    request = factory.get(APPLICATIONS_V1_URI)
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == status.HTTP_200_OK, (
        'Expected Response Code 200, received {0} instead.'.format(
            response.status_code,
        )
    )
