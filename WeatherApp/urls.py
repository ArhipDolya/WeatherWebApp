from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('weather/', views.main, name='main'),
    path('registration/', views.user_registration_view, name='user_registration_view'),
    path('login/', views.user_login_view, name='user_login_view'),
]
