from rest_framework import serializers

from applications.models import Application


class ApplicationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application.user.field.related_model
        fields = ("id", "username", "first_name", "last_name", "email", "is_active")


class ApplicationSerializer(serializers.ModelSerializer):
    user = ApplicationUserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ("id", "user", "status", "notes")
