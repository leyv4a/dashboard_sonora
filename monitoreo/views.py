from django.shortcuts import render
from django.http import JsonResponse
from dashboard.mqtt_client import latest_data, municipios_detectados, get_historial
from .models import Lectura
from datetime import datetime


def home(request):
    return render(request, "monitoreo/dashboard.html")


def api(request):
    # Si latest_data está vacío, regresamos un valor temporal
    if not latest_data:
        return JsonResponse({"hermosillo_temperatura": 0})

    return JsonResponse(latest_data)


# VISTA PRINCIPAL DEL DASHBOARD DE UN MUNICIPIO
def dashboard_view(request, municipio):
    return render(request, "monitoreo/dashboard.html", {"municipio": municipio})


# VISTA DE LISTA DE MUNICIPIOS
def municipios_view(request):
    # Obtenemos municipios desde latest_data (más actualizado que la BD)
    municipios = list(latest_data.keys())

    # Si no hay datos en caché, intentamos desde la BD
    if not municipios:
        municipios = Lectura.objects.values_list("municipio", flat=True).distinct()

    return render(request, "monitoreo/municipios.html", {"municipios": municipios})


# API GLOBAL — Todos los municipios y variables
def api_global(request):
    return JsonResponse(latest_data)


# API DE MUNICIPIOS — Lista de municipios disponibles
def api_municipios(request):
    municipios = list(latest_data.keys())
    return JsonResponse({"municipios": municipios})


# API POR MUNICIPIO - CORREGIDA para incluir timestamps
def api_municipio(request, municipio):
    """
    API que devuelve el último valor de cada tipo para un municipio
    """
    municipio = municipio.lower()

    if municipio not in latest_data:
        return JsonResponse({"error": "Municipio no encontrado"}, status=404)

    # latest_data[municipio] ya tiene el formato correcto con valor y timestamp
    return JsonResponse(latest_data[municipio])


# ============================================
# AGREGAR ESTAS DOS FUNCIONES NUEVAS AL FINAL
# ============================================

def api_municipio_historial(request, municipio):
    """
    API que devuelve el historial completo de un municipio
    Formato: {tipo: [{valor, timestamp}, {valor, timestamp}, ...]}
    """
    municipio = municipio.lower()

    # Obtener historial desde mqtt_client usando la función helper
    historial = get_historial(municipio)

    if not historial:
        return JsonResponse({"error": "No hay historial para este municipio"}, status=404)

    return JsonResponse(historial)


def api_municipio_tipo_historial(request, municipio, tipo):
    """
    API que devuelve el historial de un tipo específico
    Formato: [{valor, timestamp}, {valor, timestamp}, ...]
    """
    municipio = municipio.lower()
    tipo = tipo.lower()

    # Obtener historial de un tipo específico
    historial = get_historial(municipio, tipo)

    if not historial:
        return JsonResponse({"error": "No hay historial para este tipo"}, status=404)

    return JsonResponse({"historial": historial})


# API POR MUNICIPIO Y TIPO (temperatura, humedad, etc.)
def api_municipio_tipo(request, municipio, tipo):
    municipio = municipio.lower()
    tipo = tipo.lower()

    if municipio not in latest_data:
        return JsonResponse({"error": "Municipio no encontrado"}, status=404)

    if tipo not in latest_data[municipio]:
        return JsonResponse({"error": "Tipo no encontrado"}, status=404)

    dato = latest_data[municipio][tipo]

    # Formatear con timestamp si no lo tiene
    if isinstance(dato, dict) and 'valor' in dato:
        resultado = {tipo: dato}
    else:
        resultado = {
            tipo: {
                'valor': dato,
                'timestamp': datetime.now().isoformat()
            }
        }

    return JsonResponse(resultado)


def get_municipios(request):
    municipios = list(latest_data.keys())
    return JsonResponse({"municipios": municipios})