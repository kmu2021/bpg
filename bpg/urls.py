from django.urls import path

from . import views

urlpatterns = [    
    path('', views.init, name='bpg'),
    path('logout', views.logout, name='bpg-logout'),
]
