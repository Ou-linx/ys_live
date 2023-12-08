from django.urls import path, include

from dh_list import views

urlpatterns = [
    path('login', views.add_account),
    path('getall', views.get_all_account),    # 链接方式
    path('get', views.get_account),    # get方式

]