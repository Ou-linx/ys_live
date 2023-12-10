from django.urls import path, include

from dh_list import views

urlpatterns = [
    path('api/login', views.add_account_api),
    path('api/getall', views.get_all_account),    # 链接方式
    path('api/get', views.get_account_api),    # get方式
    path('edit',views.get_account)

]