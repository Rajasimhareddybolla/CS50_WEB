from django.urls import path

from . import views
app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("show",views.show,name="show"),
    path("details/<str:name>",views.show,name="details"),
    path("random",views.random,name="random"),
]
