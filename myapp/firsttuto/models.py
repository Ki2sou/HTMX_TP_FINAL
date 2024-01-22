from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass

class Task(models.Model):
    description = models.CharField(max_length=20)
    users = models.ManyToManyField(User,related_name='tasks')