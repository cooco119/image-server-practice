from django.urls import path
from imageviewer import views

urlpatterns = [
    path('<str:username>/workspaces/', views.GetWorkspaces.as_view(), name='workspaces'),
    path('<str:username>/workspaces/<str:name>/', views.GetImageListByName.as_view(), name='imagelist'),
    path('<str:username>/workspaces/<str:name>/images?image=<str:image_name>', views.GetImageByImageName.as_view(), name='image')
]