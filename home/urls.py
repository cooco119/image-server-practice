from django.urls import path

from home import views

urlpatterns = [
    path('signin/', views.SignInHandler.as_view(), name='signin'),
    path('notice/', views.GetNoticeHandler.as_view(), name='index'),
    path('register/', views.RegistrationHandler.as_view(), name='register'),   
]