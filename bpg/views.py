from django.shortcuts import render
from .models import UspsServices
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.dom.minidom import parse,parseString,Document
import os
import ast

# Create your views here.
def init(request):
    
    xmldoc = ET.parse(os.path.join(os.path.dirname(__file__),'services.xml'))
    root = xmldoc.getroot()
    
    serviceList = []
    
    for child in root:
        service = UspsServices()        
        service.serviceName = child.attrib['serviceName']
        service.serviceDescription = child.attrib['serviceDescription']
        service.accessFlag = eval(child.attrib['accessFlag'].title())
        service.id = child.attrib['id']
        print(service.id)     
        #serviceList[int(service.id)-1]=service   
        serviceList.append(service)
    
    return render(request, 'bpgtemplate.html',{"serviceList":serviceList})