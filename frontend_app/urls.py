from django.urls import path
from . import views

urlpatterns = [
    path('<path:filepath>', views.fileDispatcher.as_view(), name='fileDispatch'),
]