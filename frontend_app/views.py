from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, '../frontend/index.html')

def main(request):
    return render(request, 'static/frontend/main.js')

