from django.urls import path
from . import views

app_name = 'monitoreo'

urlpatterns = [
    path("", views.municipios_view, name="home"),
    path("api/", views.api, name="api"),
    path("municipios/", views.municipios_view, name="municipios"),
    path("api/data/", views.api_global, name="api_global"),
    path("api/municipios/", views.api_municipios, name="api_municipios"),
    path("api/municipios/<str:municipio>/", views.api_municipio, name="api_municipio"),
    path("api/municipios/<str:municipio>/<str:tipo>/", views.api_municipio_tipo, name="api_municipio_tipo"),
    path("municipios/", views.get_municipios),

]
