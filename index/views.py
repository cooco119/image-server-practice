from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello from image viewer index")

def Navigator(input):
    '''
    1. Verify input to be whether it calls imageviewer or imageuploader
    2. redirect to it (maybe call image-server-practice.urls?)
    '''

## TODO: add features

## maybe go SPA? current structure is MPA