from django.urls import path, include

from users import views

urlpatterns = [
    path('login', views.login),
    path('reg',views.regiset),
    path('edit',views.edituser),

]