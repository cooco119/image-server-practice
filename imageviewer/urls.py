from django.urls import path
from . import views

urlpatterns = [
    path('images/', views.GetImageHandler.as_view(), name='images')
]