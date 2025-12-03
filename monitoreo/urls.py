from django.urls import path
from . import views

app_name = 'monitoreo'

urlpatterns = [
    path('', views.home, name='home'),
    path("", views.dashboard_view, name="dashboard"),
    path("api/", views.api_datos, name="api_datos"),
    path("municipios/", views.municipios_view, name="municipios"),
]
