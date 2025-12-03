from django.urls import path
from . import views

app_name = 'monitoreo'

urlpatterns = [
    path("", views.home, name="home"),
    path("api/", views.api, name="api"),
    path("municipios/", views.municipios_view, name="municipios"),
]
