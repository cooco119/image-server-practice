from django.urls import path
from imageuploader import views

urlpatterns = [
    path('upload/', views.UploadeHandler.as_view(), name='upload'),
    path('upload/<str:bucketName>/<str:objectName>', views.UploadeHandler.as_view(), name='getUrl')
]