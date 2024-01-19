import pytest
from django.contrib.auth.models import Permission


@pytest.fixture
@pytest.mark.django_db
def super_user(django_user_model):
    user = django_user_model.objects.create_user(
        username="super-user",
        password="super-pass",
        is_superuser=True,
    )
    user.user_permissions.add(
        *Permission.objects.all()
    )
    return user


@pytest.fixture
@pytest.mark.django_db
def pure_user(django_user_model):
    return django_user_model.objects.create_user(
        username="pure-user",
        password="pure-pass",
    )
