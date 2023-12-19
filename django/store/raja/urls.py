from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("details/<int:id>",views.details,name="details"),
    path('test',views.test,name="test")
]
