from django.urls import path
from .views import index,register,password_reset,home
urlpatterns = [
    path('', index, name='login'),
path('register/', register, name='register'),
    path('password_reset/', password_reset, name='password_reset'),
    path('home/', home,name='home'),
]