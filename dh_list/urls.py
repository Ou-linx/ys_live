from django.urls import path, include
from dh_list import views

urlpatterns = [
    path('', views.account_index_page),
    path('edit', views.account_edit_page),
    path('add', views.account_add_page),
    path('api/reguards', views.ref_guards),
    path('api/edit', views.add_edit_account),
    path('api/acc_all', views.get_all_acc),
]
