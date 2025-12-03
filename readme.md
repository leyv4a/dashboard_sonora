# 🌡️ Dashboard Sonora IoT

Dashboard en tiempo real para monitoreo de variables climáticas de municipios de Sonora mediante protocolo MQTT.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![MQTT](https://img.shields.io/badge/MQTT-paho--mqtt-orange)
![License](https://img.shields.io/badge/License-Educational-yellow)

## 📸 Preview

Dashboard con monitoreo en tiempo real de temperatura, humedad y viento de municipios de Sonora.

## 🎯 Características

- ✅ **Monitoreo en tiempo real** - Actualización cada 3 segundos
- ✅ **Múltiples municipios** - Hermosillo, Guaymas, Empalme
- ✅ **Gráficas interactivas** - Chart.js con historial de 20 puntos
- ✅ **Diseño oscuro profesional** - UI moderna y responsive
- ✅ **Exportación CSV** - Descarga el historial completo
- ✅ **Dinámico** - Se adapta automáticamente a nuevos tipos de datos
- ✅ **Cache en memoria** - Historial persistente durante la sesión
- ✅ **MQTT Wildcards** - Suscripción a `sonora/#`

## 🛠️ Tecnologías

- **Backend:** Django 4.2
- **Protocolo:** MQTT (paho-mqtt)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Gráficas:** Chart.js
- **Base de datos:** SQLite (cache en memoria)
- **Broker:** test.mosquitto.org (público)

## 📦 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/leyv4a/dashboard_sonora.git
cd dashboard_sonora

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Migraciones
python manage.py migrate

# 5. Ejecutar servidor
python manage.py runserver

# 6. (Opcional) Ejecutar simulador en otra terminal
python simulador_publisher.py
```

Visita: `http://127.0.0.1:8000/`

## 📁 Estructura del Proyecto

```
dashboard_sonora/
├── 📂 dashboard/           # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── mqtt_client.py     # Cliente MQTT con cache
├── 📂 monitoreo/          # App principal
│   ├── 📂 static/monitoreo/js/
│   │   └── charts.js      # Lógica de gráficas
│   ├── 📂 templates/monitoreo/
│   │   ├── dashboard.html # Dashboard por municipio
│   │   └── municipios.html # Selector de municipios
│   ├── models.py
│   ├── views.py           # APIs y vistas
│   └── urls.py
├── requirements.txt       # Dependencias
├── manage.py
└── simulador_publisher.py # Simulador MQTT
```

## 🌐 Endpoints

### Vistas
| URL | Descripción |
|-----|-------------|
| `/` | Página principal (lista municipios) |
| `/municipios/` | Lista de municipios |
| `/dashboard/<municipio>/` | Dashboard del municipio |

### APIs
| URL | Respuesta | Descripción |
|-----|-----------|-------------|
| `/api/municipios/` | `{"municipios": [...]}` | Lista de municipios |
| `/api/municipio/hermosillo/` | `{tipo: {valor, timestamp}}` | Último valor |
| `/api/municipio/hermosillo/historial/` | `{tipo: [{valor, timestamp}...]}` | Historial completo |

## 🔧 Configuración MQTT

**Broker:** `test.mosquitto.org`  
**Puerto:** `1883`  
**Tópico:** `sonora/#`  
**Formato de mensaje:**
```json
{
    "municipio": "hermosillo",
    "tipo": "temperatura",
    "valor": 32
}
```

## 📊 Tipos de Datos Soportados

El sistema es **completamente dinámico** y soporta cualquier tipo de dato. Predefinidos:

| Tipo | Unidad | Color |
|------|--------|-------|
| 🌡️ Temperatura | °C | Rojo |
| 💧 Humedad | % | Azul |
| 💨 Viento | km/h | Verde |
| 🌧️ Precipitación | mm | Cyan |
| ☀️ Iluminación | lux | Naranja |
| ⚖️ Presión | hPa | Morado |
| 🏭 CO2 | ppm | Rojo oscuro |
| 🔊 Ruido | dB | Naranja oscuro |

## 🎨 Características del Dashboard

### Cards Dinámicas
- Se crean automáticamente para cada tipo de dato
- Diseño en grid 2x2 (responsive)
- Animaciones suaves
- Colores personalizados por tipo

### Gráficas en Tiempo Real
- Actualización cada 3 segundos
- Historial de últimos 20 puntos
- Tooltips interactivos
- Responsive

### Exportación CSV
- Botón para descargar historial completo
- Formato: `municipio_historial_YYYY-MM-DD.csv`
- Incluye: Tipo, Valor, Fecha, Hora

## 🧪 Simulador MQTT

El proyecto incluye un simulador que envía datos aleatorios:

```python
# Rango de valores
- Temperatura: 20-40°C
- Humedad: 30-90%
- Viento: 0-50 km/h

# Ciclo: 3 municipios × 3 tipos = 9 mensajes cada 2 segundos
```

## 📈 Sistema de Cache

**Cache en memoria (latest_data):**
- Almacena el último valor de cada tipo
- Incluye timestamp
- Se limpia al reiniciar Django

**Historial en memoria (historial_data):**
- Mantiene últimos 20 puntos por tipo
- Usa `deque` para eficiencia
- Auto-elimina puntos antiguos

## 🔍 Verificación del Sistema

```bash
# Verificar cache e historial
python verificar_historial.py

# Salida esperada:
# 📍 HERMOSILLO:
#    • temperatura: 20 puntos guardados
#    • humedad: 20 puntos guardados
#    • viento: 20 puntos guardados
```

## 🎓 Criterios de Evaluación

- ✅ **Funcionalidad MQTT (40%)**
  - Suscripción a `sonora/#`
  - Procesamiento de diferentes tipos
  - Manejo de errores y reconexión
  - Almacenamiento en cache

- ✅ **Dashboard y Frontend (30%)**
  - Gráficas funcionales
  - Interfaz responsive
  - Actualización automática

- ✅ **Calidad de Código (20%)**
  - Estructura organizada
  - Documentación
  - Buenas prácticas
  - Manejo de excepciones

- ✅ **Funcionalidades Extra (10%)**
  - Exportación CSV
  - Diseño profesional
  - Historial persistente

## 🐛 Troubleshooting

**Problema:** No aparecen datos  
**Solución:** 
1. Verifica que el cliente MQTT esté conectado (busca ✅ en consola)
2. Ejecuta el simulador: `python simulador_publisher.py`
3. Espera 5 segundos y recarga

**Problema:** Error de conexión MQTT  
**Solución:** 
- Verifica tu conexión a internet
- El broker público puede estar saturado, intenta más tarde
- Considera usar otro broker: `broker.hivemq.com`

**Problema:** Las gráficas no cargan  
**Solución:**
1. Abre DevTools (F12) → Console
2. Busca errores JavaScript
3. Verifica que `charts.js` esté en `static/monitoreo/js/`
4. Ejecuta: `python manage.py collectstatic`

## 📝 TODO / Mejoras Futuras

- [ ] Autenticación de usuarios
- [ ] Base de datos persistente (PostgreSQL)
- [ ] Redis para cache en producción
- [ ] WebSockets para comunicación bidireccional
- [ ] Sistema de alertas (umbrales)
- [ ] Panel de administración mejorado
- [ ] Dockerización
- [ ] Tests unitarios
- [ ] CI/CD con GitHub Actions

## 👨‍💻 Autor

**Luis Leyva**  
Proyecto final - Curso de Internet de las Cosas  
Universidad de Sonora - 2025

## 📄 Licencia

Este proyecto es para fines educativos del curso de IoT.

---

⭐ Si te gustó el proyecto, dale una estrella en GitHub!