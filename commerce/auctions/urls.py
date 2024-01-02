from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.add,name="add"),
    path("bid",views.bid,name="bid"),
    path("watch_list",views.watch_list,name="watch_list"),
    path("catogeries:<str:cat>",views.catogerie,name="catogerie"),
]
