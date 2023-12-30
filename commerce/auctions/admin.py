from django.contrib import admin
from .models import items,User,bids
# Register your models here.
admin.site.register(User)
admin.site.register(items)
admin.site.register(bids)
