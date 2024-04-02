from django.urls import path
from .views import *

urlpatterns = [
    path('delete-receipe/<int:id>', delete_receipe, name="delete_receipe"),
    path('updat/<int:id>', update_receipe, name="updated"),
    path('loginn', login_page, name="login"),
    path('register', register, name="register"),
    path('logout', logout_page, name="logout_page"),
    path(route="students", view=get_students, name="get_students"),
    path(route="seemarks/<student_id>", view=see_marks, name="seeMarks"),
]
