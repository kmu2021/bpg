from django.urls import path

from . import views

urlpatterns = [    
    path('', views.init, name='bpgrg'),
    path('logout', views.logout, name='bpgrg-logout'),
]
