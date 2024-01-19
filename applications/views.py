from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from applications.models import Application
from applications.permissions import ApplicationObjectPermission
from applications.serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated, ApplicationObjectPermission)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
