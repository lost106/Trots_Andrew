from django.urls import path

from . import views

app_name = 'coming'
urlpatterns = [
    path('', views.home, name='home'),
    path('coming/', views.coming, name='coming'),
]
