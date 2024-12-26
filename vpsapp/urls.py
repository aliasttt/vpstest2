from django.urls import path
from . import views

app_name = 'vpsapp'



urlpatterns = [
    path('', views.home, name='home'),
    path('contactus', views.Contactus, name='contactus'),
    path('aboutus', views.Aboutus, name='aboutus'),
    path('rooms', views.Rooms, name='rooms'),
    
]