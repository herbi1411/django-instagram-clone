from django.urls import path, include
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("update/", views.update, name="update"),
    path("<int:pk>/profile/", views.profile, name="profile"),
    path('<int:pk>/follow', views.follow, name='follow'),
]
