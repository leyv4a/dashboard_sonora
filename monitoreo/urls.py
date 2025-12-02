from django.urls import path
from . import views

app_name = 'monitoreo'

urlpatterns = [
    path('', views.home, name='home'),
]
