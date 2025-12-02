from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'monitoreo/dashboard.html')

# Más adelante cambiaremos esto por render(request, 'monitoreo/dashboard.html', {...})
