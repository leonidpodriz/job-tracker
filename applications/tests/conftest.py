import pytest


@pytest.fixture
@pytest.mark.django_db
def user(django_user_model):
    yield django_user_model.objects.create_user(
        username="pure-user",
        password="pure-pass",
    )
    django_user_model.objects.filter(username="pure-user").delete()
