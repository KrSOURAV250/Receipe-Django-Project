from django.urls import path
from .views import *

urlpatterns = [
    path('', receipes),
    path('delete-receipe/<int:id>', delete_receipe, name="delete_receipe"),
    path('updat/<int:id>', update_receipe, name="updated"),
    path('login', login, name="login"),
    path('register', register, name="register")
]
