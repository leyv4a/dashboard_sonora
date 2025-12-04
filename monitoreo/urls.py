from django.urls import path
from . import views

app_name = 'monitoreo'

urlpatterns = [
    # Vista principal - lista de municipios
    path("", views.municipios_view, name="home"),

    # Vista del dashboard de un municipio específico
    path("dashboard/<str:municipio>/", views.dashboard_view, name="dashboard"),

    # Vista de municipios
    path("municipios/", views.municipios_view, name="municipios"),

    # Vista del mapa
    path("mapa/", views.mapa_view, name="mapa"),

    # APIs
    path("api/", views.api, name="api"),
    path("api/data/", views.api_global, name="api_global"),
    path("api/municipios/", views.api_municipios, name="api_municipios"),
    path("api/municipio/<str:municipio>/", views.api_municipio, name="api_municipio"),
    path("api/municipios/<str:municipio>/<str:tipo>/", views.api_municipio_tipo, name="api_municipio_tipo"),

    # APIs - Historial (todos los puntos guardados)
    path("api/municipio/<str:municipio>/historial/", views.api_municipio_historial, name="api_municipio_historial"),
    path("api/municipio/<str:municipio>/<str:tipo>/historial/", views.api_municipio_tipo_historial, name="api_municipio_tipo_historial"),
]
