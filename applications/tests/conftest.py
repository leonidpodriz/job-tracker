import pytest


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='test-user',
        password='test-pass',
    )
