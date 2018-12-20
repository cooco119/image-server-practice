from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello from image viewer index")

def fetch_image():
    '''
    get image from db server
    '''

def update_panel():
    '''
    update the image viewer panel
    '''

def draw_panel():
    '''
    draw a panel for showing images
    '''

def click_handler():
    '''
    when clicks, magnify image in new, upper layer
    '''

def 