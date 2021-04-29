from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

app_name = 'map'
urlpatterns = [
    path('', views.index),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('new_store/', views.registerMag, name='registerMag'),
    path('map/', views.show_map, name='map')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)