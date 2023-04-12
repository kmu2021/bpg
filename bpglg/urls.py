from django.urls import path

from . import views

urlpatterns = [    
    path('', views.init, name='bpglg'),
    path('logout', views.logout, name='bpglg-logout'),    
    path('getotp', views.generateotp, name='bpglg-getotp'),    
    path('usermanagement', views.usermgmt, name='bpglg-usermgmt'),
    path('resendinvitation', views.resendinvite, name='bpglg-resendinvite'),
    path('getuseraccesscontrolform', views.get_user_access_control_form, name='bpglg-user-get-user-access-control-form'),
    path('setuseraccesscontrolform', views.get_user_access_control_form, name='bpglg-user-set-user-access-control-form'),
    path('testemail', views.testemail, name='bpglg-testemail')
]
