from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'monitoreo/dashboard.html')

# Más adelante cambiaremos esto por render(request, 'monitoreo/dashboard.html', {...})
from django.shortcuts import render
from django.http import JsonResponse
from dashboard.mqtt_client import latest_data
from .models import Lectura

def dashboard_view(request):
    return render(request, "monitoreo/dashboard.html")

def api_datos(request):
    return JsonResponse(latest_data)

def municipios_view(request):
    municipios = Lectura.objects.values_list("municipio", flat=True).distinct()
    return render(request, "monitoreo/municipios.html", {"municipios": municipios})
