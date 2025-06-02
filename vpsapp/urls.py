from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'vpsapp'



urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)