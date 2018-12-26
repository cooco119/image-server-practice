from django.urls import path
from imageuploader import views

urlpatterns = [
    path('upload/', views.UploadeHandler.as_view(), name='getUrl')
]