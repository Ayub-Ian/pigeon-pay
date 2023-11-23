from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
import datetime

class User(AbstractBaseUser):
    
    username = None
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20)
    image = models.FileField(upload_to="media/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    @property
    def is_superuser(self):
        return self.is_admin


    def has_perm(self, perm, obj=None):
       return self.is_admin
    
    def has_module_perms(self, app_label):
       return self.is_admin
    
   

    def save_last_login(self) -> None:
        self.last_login = datetime.now()
        self.save()
