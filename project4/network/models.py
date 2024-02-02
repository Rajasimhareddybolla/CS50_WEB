from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    following = models.ManyToManyField('self', blank=True, related_name="followers" , symmetrical=False)
class post(models.Model):
    content = models.TextField(max_length=1000)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.IntegerField(editable=True)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       return str(self.time)+"  "+self.user.username
class link(models.Model):
    post =models.ForeignKey(post,on_delete=models.CASCADE)
    c_user = models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True)
    comment = models.CharField(max_length=1000,null=True,blank=True)
    like = models.BooleanField(default=False)
    def __str__(self):
        return self.c_user.username+" on "+str(self.post.time)