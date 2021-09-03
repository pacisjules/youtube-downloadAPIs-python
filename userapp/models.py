from django.db import models
from django.contrib.auth.models import  PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_active, is_staff, is_superuser, **extra_fields):
        
        if not username:
            raise ValueError("Username is not valid")
        email=self.normalize_email(email)
        user=self.model(username=username, email=email,  is_active=True, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email,password, **extra_fields):
        return self._create_user(username, email,password, is_active=False, is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, is_active=True, is_staff=True, is_superuser=True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    
    username=models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=250, unique=True)
    first_name=models.CharField(max_length=255, blank=True, null=True)
    last_name=models.CharField(max_length=30, blank=True, null=True)
    phone=models.CharField(max_length=13)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)
    receive_newsletter=models.BooleanField(default=False)
    birth_date=models.DateTimeField(blank=True, null=True)
    address=models.CharField(max_length=300, blank=True, null=True)
    city=models.CharField(max_length=300, blank=True, null=True)
    about_me=models.CharField(max_length=300, blank=True, null=True)
    type=models.CharField(max_length=300, blank=True, null=True)
    password=models.CharField(max_length=255)
    #profile_img=models.ImageField(null=True)

    objects = UserManager()

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email']

