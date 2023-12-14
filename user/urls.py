from django.urls import path, include
from user import views

urlpatterns = [
    path('login', views.user_login_page),
    path('regiset', views.user_regiset_page),
]
