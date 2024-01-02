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
    # category = models.Choices(("Comedy":"Comendy","Action"))
    def __str__(self):
        return self.Title
class bids(models.Model):
    prodouct = models.ForeignKey(items,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    bid  = models.IntegerField(max_length=1000,null=True,default=0)
    comments = models.CharField(max_length=500,null=True)
    whishlist = models.BooleanField(default=False)

    def __str__(self) :
        return self.prodouct.Title +"bid by "+self.user.last_name+"bidded this one for "+(str)(self.bid)
class catogeries(models.Model):
    catogeries={"Electronics":"Electronics","Fashion":"Fashion","Home & Kitchen":"Home & Kitchen","Books & Media":"Books & Media","Health & Beauty":"Health & Beauty","Sports & Outdoors":"Sports & Outdoors","Toys & Games":"Toys & Games","Grocery & Gourmet Food":"Grocery & Gourmet Food"}
    prodouct = models.ForeignKey(items,on_delete=models.CASCADE)
    catogery = models.CharField(max_length=100,choices=catogeries,)
    def __str__(self):
        return f"{self.prodouct.Title } is in {self.catogery}"
