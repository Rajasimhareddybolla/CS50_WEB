from django.db import models

# Create your models here.
class prod(models.Model):
    name = models.CharField(max_length = 255)
    price = models.IntegerField()
    url = models.ImageField(upload_to="PICS")
# python manage.py makemigrations
#python manage.py sqlmigrate appname migration_no
#python manage.py sqlmigrate task 0001
#python manage.py migrate
# # change the settings like this
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME':  'cs50',
#         'USER':'postgres',
#         'PASSWORD':'raja',
#         'HOST':'localhost',
#     }
# }
    def __str__(self):
        return self.name