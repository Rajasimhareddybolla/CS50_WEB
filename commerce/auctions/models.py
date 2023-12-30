from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser,models.Model):
    pass
class items(models.Model):
    Title = models.CharField(max_length = 63)
    Discription = models.CharField(max_length = 255)
    Ammount = models.IntegerField()
    Image = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="seller")
    relations = models.ManyToManyField(User,through="bids" )

    def __str__(self):
        return self.Title
class bids(models.Model):
    prodouct = models.ForeignKey(items,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    bid  = models.CharField(max_length=1000,null=True)
    comments = models.CharField(max_length=500,null=True)
    whishlist = models.BooleanField(blank= True,null=True)

    def __str__(self) :
        return self.prodouct.Title