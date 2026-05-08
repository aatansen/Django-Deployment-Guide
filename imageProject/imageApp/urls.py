from django.urls import path
from imageApp.views import *

urlpatterns = [
    # auth
    path('signup/',signup,name='signup'),
    path('',signin,name='signin'),
    path('signout/',signout,name='signout'),

    # users
    path('dashboard/',dashboard,name='dashboard'),
    path('adduser/',adduser,name='adduser'),
    path('users/',users,name='users'),
    path('deleteuser/<str:id>',deleteuser,name='deleteuser'),
]
