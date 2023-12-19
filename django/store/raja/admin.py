from django.contrib import admin
from .models import member,info
# Register your models here.
#which change the display of the sqlite database to the coloumns what we want
class adminview(admin.ModelAdmin):
    list_display=["firstname","lastname","id"]
class infoview(admin.ModelAdmin):
    list_display= ["prodouct_name","seller_id"]
admin.site.register(member,adminview)
admin.site.register(info,infoview)