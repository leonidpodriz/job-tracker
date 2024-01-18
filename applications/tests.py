from rest_framework import status, routers
from rest_framework.test import APIRequestFactory
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

    for request, args in requests:
        response = view(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            'Expected Response Code 401, received {0} instead. (Method: {1})'.format(
                response.status_code,
                request.method
            )
        )
