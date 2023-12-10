from django.urls import path, include

from dh_list import views

urlpatterns = [
    path('api/edit', views.add_account_api),
    path('api/delete', views.del_account_api),
    path('api/getall', views.get_all_account_api),
    path('api/get', views.get_account_api),
    path('edit', views.edit_account),
    path('', views.get_all_account_api)
]
