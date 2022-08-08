from django.urls import path

from . import processData

urlpatterns = [    
    path('processForm',processData.process,name='bpgrg-process-data'),
]
