from django.urls import path, include

from users import views

urlpatterns = [
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('reg', views.regiset),
    path('edit', views.edituser),

]
