from django.contrib.auth        import get_user_model

from rest_framework             import status
from rest_framework.viewsets    import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response    import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models                    import User
from .serializers               import RegisterUserSerializer

class UserGenericViewSet(GenericViewSet):
    permission_classes = [AllowAny]
    queryset           = get_user_model()
    lookup_field       = 'id'

    def create(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user  = serializer.save()
        token = RefreshToken.for_user(user)
        data  = {'refresh': str(token), 'access': str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)