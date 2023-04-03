from django.urls import path

from . import views

urlpatterns = [    
    path('', views.init, name='bpglg'),
    path('logout', views.logout, name='bpglg-logout'),    
    path('getotp', views.generateotp, name='bpglg-getotp'),    
    path('usermanagement', views.usermgmt, name='bpglg-usermgmt'),
    path('resendinvitation', views.resendinvite, name='bpglg-resendinvite'),
    path('testemail', views.testemail, name='bpglg-testemail')
]
