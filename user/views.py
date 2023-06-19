from user.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from user.permissions import IsOwnerUserOrAdmin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Overwrites the get_permissions method to return individual permission classes depending on the performed action.
        This leads to following permission behavior:
        Everyone is permitted to perform "create" action.
        Admin users and the owner users of an objects are permitted to perform "retrieve", "update" and "partial_update" actions.
        Admin users are permitted to perform "list" and "destroy" action.
        """
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwnerUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
