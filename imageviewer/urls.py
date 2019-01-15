from django.urls import path
from imageviewer import views

urlpatterns = [
    path('<str:username>/workspaces/',
         views.GetWorkspaces.as_view(),
         name='workspaces'),

    path('<str:username>/workspaces/<str:targetname>/',
         views.GetImageListByName.as_view(),
         name='imagelist'),

    path('images/<str:bucketName>/<str:objectName>/',
         views.GetPresignedImageGetUrl.as_view(),
         name='geturl')
]