from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser,models.Model):
    pass
class items(models.Model):
    Title = models.CharField(max_length = 63)
    Discription = models.CharField(max_length = 255)
    Ammount = models.IntegerField()
    Image = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="books")
