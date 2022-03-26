from django.urls import path
from newsapp.views import user_login, user_logout, post_story, get_story, del_story, user_register

urlpatterns = [
    path('api/login/', user_login),
    path('api/logout/', user_logout),
    path('api/register/', user_register),
    path('api/poststory/', post_story),
    path('api/getstory/', get_story),
    path('api/deletestory/', del_story),
]
