from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'vpsapp'



urlpatterns = [
    path('', views.home, name='home'),
    path('contactus', views.Contactus, name='contactus'),
    path('aboutus', views.Aboutus, name='aboutus'),
    path('rooms', views.Rooms, name='rooms'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)