from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import options
from rest_framework import serializers
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.request import Request
from rest_framework.views import APIView

FIELD_PERMISSION_FORMAT = "{app_label}.set_{model_name}_{field_name}"


def get_field_permission(model_cls: models.Model, field_name: str) -> tuple[str, str]:
    """
    Returns the permission code and the permission name for a given model field with description.
    """
    meta = get_model_options(model_cls)

    return FIELD_PERMISSION_FORMAT.format(
        app_label=meta.app_label,
        model_name=meta.model_name,
        field_name=field_name,
    ), f"Can change {meta.model_name} {field_name}"


def get_model_options(model_cls: models.Model) -> options.Options:
    meta = getattr(model_cls, "_meta")

    if not isinstance(meta, options.Options):
        raise ValueError("Model does not have a Meta class")

    return meta


def has_user_protected_field_permission(user: AbstractUser, obj: models.Model, field_name: str) -> bool:
    return user.has_perm(get_field_permission(obj, field_name)[0])


class GeneralObjectPermission(DjangoObjectPermissions):
    perms_map = {
        **DjangoObjectPermissions.perms_map,
        'GET': ['%(app_label)s.view_%(model_name)s'],
    }

    protected_fields = tuple()
    _update_methods = ("PATCH", "PUT")
    _create_methods = ("POST",)

    def has_object_permission(self, request: Request, view: APIView, obj: any):
        has_permission = super().has_object_permission(request, view, obj)

        if not has_permission:
            return False

        serializer = self.get_serializer(view)
        user = request.user

        if not isinstance(user, AbstractUser):
            return False

        for key in request.data.keys():
            serializer_field = serializer.fields.get(key, None)
            if serializer_field is None:
                continue

            field_name = serializer_field.source_attrs[-1]
            if field_name in self.protected_fields and not has_user_protected_field_permission(user, obj, field_name):
                return False

        return True

    @classmethod
    def get_serializer(cls, view: APIView) -> serializers.Serializer:
        get_serializer = getattr(view, "get_serializer", None)

        if get_serializer is None:
            raise ValueError("View does not have a get_serializer method")

        serializer = get_serializer()

        if not isinstance(serializer, serializers.Serializer):
            raise ValueError("View's get_serializer method did not return a Serializer")

        return serializer
