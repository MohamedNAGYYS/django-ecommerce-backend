from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password = None):
        if not email:
            raise ValueError("Users must have an email address.")
        
        user = self.model(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(first_name, last_name, email, password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.role = Users.RoleChocies.ADMIN
        user.save(using=self._db)
        return user

    
class Users(AbstractBaseUser, PermissionsMixin):
    class RoleChocies(models.TextChoices):
        ADMIN = 'Admin'
        CUSTOMER = 'Customer'
    role=models.CharField(max_length=20,choices=RoleChocies.choices,default=RoleChocies.CUSTOMER)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def __str__(self):
        return self.email
    
