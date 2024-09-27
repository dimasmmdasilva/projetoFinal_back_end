from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Localização")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name="Foto de Perfil")
