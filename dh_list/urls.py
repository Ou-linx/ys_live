from django.urls import path, include
from dh_list import views

urlpatterns = [
    path('', views.account_index_page),
    path('edit', views.account_edit_page),
    path('add', views.account_add_page),
]
