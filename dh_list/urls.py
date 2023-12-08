from django.urls import path, include

from dh_list import views

urlpatterns = [
    path('login', views.add_account),
    path('get/<acc_id>', views.get_account),    # 链接方式
    path('get', views.get_account1),    # get方式

]