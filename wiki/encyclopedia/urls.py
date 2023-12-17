from django.urls import path

from . import views
app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("details/<str:name>",views.show,name="details")
]
