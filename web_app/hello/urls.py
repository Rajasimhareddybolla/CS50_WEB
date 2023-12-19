from django.urls import path
from . import views
urlpatterns=[
  path("",views.index,name="index"),
  path("wish",views.wish,name="inter"),
  path("<str:name>",views.greet,name="greet")
  # the <str:name> come in to play if no route match then it come to name
  
]
