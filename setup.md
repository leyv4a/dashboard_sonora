# 🚀 Guía de Instalación - Dashboard Sonora IoT

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## 🔧 Instalación

### 1. Clonar el repositorio (si aplica)

```bash
git clone https://github.com/leyv4a/dashboard_sonora.git
cd dashboard_sonora
```

### 2. Crear entorno virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Django

**Crear migraciones:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Crear superusuario (opcional):**
```bash
python manage.py createsuperuser
```

**Recolectar archivos estáticos:**
```bash
python manage.py collectstatic --noinput
```

## ▶️ Ejecutar el Proyecto

### 1. Iniciar el servidor Django

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

### 2. Iniciar el cliente MQTT

**Opción A: Automático con Django**

El cliente MQTT se inicia automáticamente cuando Django arranca. Verifica en la consola que veas:

```
✅ Conectado exitosamente al broker MQTT
📡 Suscrito al tópico: sonora/#
```

**Opción B: Manual (si es necesario)**

En otra terminal, con el entorno virtual activado:

```bash
python -c "from dashboard.mqtt_client import start_mqtt; start_mqtt(); import time; time.sleep(999999)"
```

### 3. (Opcional) Ejecutar simulador MQTT

En otra terminal:

```bash
python simulador_publisher.py
```

## 🌐 Acceder a la Aplicación

- **Lista de Municipios:** http://127.0.0.1:8000/
- **Dashboard de Hermosillo:** http://127.0.0.1:8000/dashboard/hermosillo/
- **API Global:** http://127.0.0.1:8000/api/data/
- **API por Municipio:** http://127.0.0.1:8000/api/municipio/hermosillo/
- **Historial:** http://127.0.0.1:8000/api/municipio/hermosillo/historial/
- **Admin Django:** http://127.0.0.1:8000/admin/

## 🔍 Verificar Instalación

### Verificar que el MQTT funciona:

```bash
python verificar_historial.py
```

Deberías ver:
```
📍 HERMOSILLO:
   • temperatura: 5 puntos guardados
   • humedad: 5 puntos guardados
   • viento: 5 puntos guardados
```

### Verificar las APIs:

```bash
# En tu navegador o con curl:
curl http://127.0.0.1:8000/api/municipios/
curl http://127.0.0.1:8000/api/municipio/hermosillo/
```

## 🐛 Solución de Problemas

### Error: "No module named 'paho'"
```bash
pip install paho-mqtt
```

### Error: "No se puede conectar al broker MQTT"
Verifica que tengas conexión a internet. El broker público `test.mosquitto.org` requiere conexión.

### Error: "Port already in use"
Cambia el puerto de Django:
```bash
python manage.py runserver 8080
```

### Los datos no aparecen en el dashboard
1. Verifica que el cliente MQTT esté conectado (mira la consola)
2. Ejecuta el simulador: `python simulador_publisher.py`
3. Espera 3-5 segundos y recarga el navegador

## 📦 Estructura del Proyecto

```
dashboard_sonora/
├── dashboard/              # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   └── mqtt_client.py     # Cliente MQTT
├── monitoreo/             # Aplicación principal
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── static/
│   │   └── monitoreo/
│   │       └── js/
│   │           └── charts.js
│   └── templates/
│       └── monitoreo/
│           ├── dashboard.html
│           └── municipios.html
├── requirements.txt
├── manage.py
└── simulador_publisher.py
```

## 🎯 Endpoints Disponibles

| Endpoint | Descripción |
|----------|-------------|
| `/` | Lista de municipios |
| `/municipios/` | Lista de municipios (mismo) |
| `/dashboard/<municipio>/` | Dashboard del municipio |
| `/api/municipios/` | Lista de municipios (JSON) |
| `/api/municipio/<municipio>/` | Último valor de cada tipo |
| `/api/municipio/<municipio>/historial/` | Historial completo |
| `/api/municipio/<municipio>/<tipo>/` | Último valor de un tipo |
| `/api/municipio/<municipio>/<tipo>/historial/` | Historial de un tipo |

## 📝 Notas

- Los datos se guardan en **memoria** mientras Django esté corriendo
- Al reiniciar Django, se pierden los datos históricos
- El historial mantiene los últimos **20 puntos** por tipo
- Las actualizaciones ocurren cada **3 segundos**
- El simulador envía datos cada **2 segundos**

## 🆘 Soporte

Si tienes problemas, verifica:
1. Versión de Python: `python --version` (debe ser 3.8+)
2. Dependencias instaladas: `pip list`
3. Logs de Django en la consola
4. Logs del cliente MQTT (busca ✅ o ❌)

## 📄 Licencia

Este proyecto es para fines educativos del curso de IoT.