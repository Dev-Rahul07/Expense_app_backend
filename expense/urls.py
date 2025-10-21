from django.urls import path
from .views import *
urlpatterns = [
    path('signup/',signup,name = 'signup'),
    path('login/',login,name = 'login'),
    path('add_expense/',add_expense,name = 'add_expense'),
    path('manage_expense/<int:UserId>/',manage_expense,name = 'manage_expense'),
    path('edit_expense/<int:Id>/',edit_expense,name = 'edit_expense'),
    path('delete_expense/<int:Id>/',delete_expense,name = 'delete_expense'),
    path('change_password/<str:UserName>/',change_password,name ='change_password'),
    path('forgot_password/<str:UserName>/', forgot_password),
]