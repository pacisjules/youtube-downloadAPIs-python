from django import urls
from django.contrib import admin
from django.urls import path, include
from userapp.views import UserList, CustomAuthToken,UserList


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    #YoutubeAppApi
    path('ytd/', include('youtubeapp.urls')),

    path('user/v1', UserList.as_view(), name="user"),
    path('admin/', admin.site.urls),
    path('custom_login', CustomAuthToken.as_view(), name="user login"),

    path('auth/register', UserList.as_view(), name='UserRegister'),
    path('auth/login', TokenObtainPairView.as_view(), name='Bear Jwt only Userlogin'),
    path('auth/token-refresh', TokenRefreshView.as_view(), name='Usertokenrefresh'),
]
