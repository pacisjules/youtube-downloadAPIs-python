from os import access
from django.db.models.query import QuerySet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .models import User
from .serializer import UserDetailsSerializer
from rest_framework.permissions import AND, AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import json



from rest_framework.response import Response

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from rest_framework_simplejwt.tokens import RefreshToken



# For Filter
from rest_framework.filters import SearchFilter
# Create your views here.



class UserList(generics.ListCreateAPIView):
    #authentication_classes=[authentication.TokenAuthentication]
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class=UserDetailsSerializer

    # Search
    filter_backends = [SearchFilter]
    search_fields = ['username']


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})

        
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        token, created = Token.objects.get_or_create(user=user)


        return Response({
            'auto_simple_token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'phone': user.phone,
            'type':user.type,
            'Created':created,
            'Jwt_refresh': str(refresh),
            'Jwt_access_token': str(refresh.access_token),
        })



