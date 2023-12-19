from django.db import models

# Create your models here.
class member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    prod = models.CharField(max_length = 255)
    # which can change the default view in django admin site which can change 
    # member0,member1 to their first and last name
    def __str__(obj):
        return obj.firstname+"  "+obj.lastname
class info(models.Model):
    prodouct_name = models.CharField(max_length = 255)
    price = models.IntegerField()
    seller_id  = models.IntegerField(("seller id"))