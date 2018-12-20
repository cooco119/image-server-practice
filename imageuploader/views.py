from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello from image uploader index")

def upload_handler(request):
    '''
    1. parse json
    2. Make Image model at the end of the Image field
    3. Save
    4. return response of success or failure
    '''