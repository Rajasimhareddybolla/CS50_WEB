
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new",views.add,name="post"),
    path('profile/<str:name>',views.index,name="profile"),
    path('following',views.following,name="following"),
    path('page=<int:page_no>',views.index,name="paginator"),
    path('profile/page=<int:page_no>',views.following,name="paginator"),
    path('like',views.like, name='like'),
    path('profile/like',views.like, name='like'),
    path('edit',views.edit_post,name="edit"),
    path('follow_trigger',views.follow_trigger)
    
]
