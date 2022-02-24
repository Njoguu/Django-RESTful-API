from locale import normalize
from django import db
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)

# Create your models here.
class UserManager(BaseUserManager):
    
    def createUser(self,username,email,password=None):
        if username is None:
            raise TypeError('Users should have a username!')
        if email is None:
            raise TypeError('User should have an active email!')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def createSuperUser(self,username,email,password=None):
        if password is None:
            raise TypeError('Password should be empty!')

        user = self.createUser(username,email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=155, unique=True, db_index=True)
    email = models.EmailField(max_length=155, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIElDS = ['username']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    