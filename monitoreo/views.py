from django.shortcuts import render
from django.http import JsonResponse
from dashboard.mqtt_client import latest_data
from .models import Lectura

def home(request):
    return render(request, "monitoreo/dashboard.html")

def api(request):
    # Si latest_data está vacío, regresamos un valor temporal
    if not latest_data:
        return JsonResponse({"hermosillo_temperatura": 0})

    return JsonResponse(latest_data)

def municipios_view(request):
    municipios = Lectura.objects.values_list("municipio", flat=True).distinct()
    return render(request, "monitoreo/municipios.html", {"municipios": municipios})
