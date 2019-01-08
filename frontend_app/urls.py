from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    # path('static/frontend/main.js', views.main)
]