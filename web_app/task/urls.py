from django.urls import path
from . import views
app_name= "task"
#<a herf="{%url 'task:index'%}">index </a>
urlpatterns = [
    path("",views.index,name="index"),
    path("add",views.add,name="add")
]

