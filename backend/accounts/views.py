from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import MeSerializer


class UserView(APIView):

    def get_permissions(self):
        action = getattr(self, "action", None)
        if action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)