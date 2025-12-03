from django.shortcuts import render
from django.http import JsonResponse
from dashboard.mqtt_client import latest_data, municipios_detectados
from .models import Lectura

def home(request):
    return render(request, "monitoreo/dashboard.html")

def api(request):
    # Si latest_data está vacío, regresamos un valor temporal
    if not latest_data:
        return JsonResponse({"hermosillo_temperatura": 0})

    return JsonResponse(latest_data)

def dashboard_view(request, municipio):
    return render(request, "monitoreo/dashboard.html", {"municipio": municipio})

def municipios_view(request):
    municipios = Lectura.objects.values_list("municipio", flat=True).distinct()
    return render(request, "monitoreo/municipios.html", {"municipios": municipios})

# API GLOBAL — Todos los municipios y variables
def api_global(request):
    return JsonResponse(latest_data)


# API DE MUNICIPIOS — Lista de municipios disponibles
def api_municipios(request):
    municipios = list(latest_data.keys())
    return JsonResponse({"municipios": municipios})


# API POR MUNICIPIO
def api_municipio(request, municipio):
    municipio = municipio.lower()

    if municipio not in latest_data:
        return JsonResponse({"error": "Municipio no encontrado"}, status=404)

    return JsonResponse(latest_data[municipio])


# API POR MUNICIPIO Y TIPO (temperatura, humedad, etc.)
def api_municipio_tipo(request, municipio, tipo):
    municipio = municipio.lower()
    tipo = tipo.lower()

    if municipio not in latest_data:
        return JsonResponse({"error": "Municipio no encontrado"}, status=404)

    if tipo not in latest_data[municipio]:
        return JsonResponse({"error": "Tipo no encontrado"}, status=404)

    return JsonResponse({tipo: latest_data[municipio][tipo]})

def get_municipios(request):
    municipios = list(latest_data.keys())
    return JsonResponse({"municipios": municipios})