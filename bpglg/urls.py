from django.urls import path

from . import views

urlpatterns = [    
    path('', views.init, name='bpglg'),
    path('logout', views.logout, name='bpglg-logout'),
    path('search', views.search, name='bpglg-search'),
    path('getotp', views.generateotp, name='bpglg-getotp'),    
    path('usermanagement', views.usermgmt, name='bpglg-getotp'),
    path('resendinvitation', views.resendinvite, name='bpglg-resendinvite'),
    path('testemail', views.testemail, name='bpglg-testemail')
]
