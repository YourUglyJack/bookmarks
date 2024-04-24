from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)  # null=True 允许存储null
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)  # blank=True 可以为空，填写表单的时候也可以为空

    def __str__(self):
        return f'Profile for user {self.user.username}'
