import os
import uuid

from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User,AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models


def photo_upload(instance, filename):
    """Gives a unique path to the saved photo in models.
    Arguments:
        instance: the photo itself, it is not used in this
                  function but it's required by django.
        filename: the name of the photo sent by user, it's
                  used here to get the format of the file.

    Returns:
        The unique path that the file will be stored in the DB.
    """

    return 'users/{0}.{1}'.format(uuid.uuid4().hex, os.path.splitext(filename))

class customUserManager(BaseUserManager):
    """Custom user Manager class to create users"""

    def create_user(self,first_name, last_name,username,email,password):
        if not first_name:
            raise ValueError("User must have an firstname address")
        if not last_name:
            raise ValueError("User must have a last name")
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password,username,first_name,last_name,):
        user = self.create_user(
            email=self.normalize_email(email=email),
            password=password,
            username=username,
            first_name = first_name,
            last_name = last_name,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class customUser(AbstractBaseUser, PermissionsMixin):
    
    email            = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username         = models.CharField(max_length=50,null= False)
    first_name       = models.CharField(max_length=50,null= False)
    last_name        = models.CharField(max_length=50,null= False)
    username         = models.CharField(max_length=50,null= False)
    date_joined      = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login       = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin         = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_staff         = models.BooleanField(default=False)
    is_superuser     = models.BooleanField(default=False)

    
    
    USERNAME_FIELD = "email"
    EMAIL_FILED = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username']

    objects = customUserManager()


    def has_perm(self,perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserProfileModel(models.Model):

    """The Model of the User Profile."""

    account          = models.OneToOneField(customUser, on_delete=models.CASCADE, related_name="profile")
    profile_photo    = models.ImageField(upload_to=photo_upload, null=True)
    phone_number     = models.BigIntegerField()

    def __str__(self):
        return self.account.username
    


class UserAddressModel(models.Model):
    """The Model of the User's address."""

    address_type_choices = [
        ('H', 'House'),
        ('O', 'Office'),
        ('A', 'Apartment')
    ]

    user = models.ForeignKey(to=UserProfileModel, related_name="addresses", on_delete=models.CASCADE)
    sort = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True)  # only used in the admin dashboard
    city = models.CharField(max_length=255, blank=True)  # only used in the admin dashboard
    area = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=address_type_choices)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    floor = models.PositiveIntegerField(default=1)
    apartment_no = models.PositiveIntegerField(default=1)
    special_notes = models.TextField(blank=True)
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[
        MaxValueValidator(180),
        MinValueValidator(-180)
    ])
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[
        MaxValueValidator(90),
        MinValueValidator(-90)
    ])

    class Meta:
        unique_together = ("user", "sort")
        ordering = ['sort']

    def __str__(self):
        return self.title
