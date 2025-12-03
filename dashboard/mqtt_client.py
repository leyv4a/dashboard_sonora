import json
import paho.mqtt.client as mqtt
from datetime import datetime
from collections import deque

# Configuración del broker MQTT
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "sonora/#"

# CACHE de datos - Almacena el último valor recibido de cada tipo
# Estructura: latest_data[municipio][tipo] = {"valor": X, "timestamp": "..."}
latest_data = {}

# HISTORIAL de datos - Almacena los últimos N valores para gráficas
# Estructura: historial_data[municipio][tipo] = deque([{valor, timestamp}, ...])
historial_data = {}

# Configuración del historial
MAX_HISTORY_POINTS = 20  # Número máximo de puntos a guardar por tipo

# Lista dinámica de municipios detectados
municipios_detectados = set()


def on_connect(client, userdata, flags, rc):
    """
    Callback cuando el cliente se conecta al broker MQTT
    """
    if rc == 0:
        print("✅ Conectado exitosamente al broker MQTT")
        client.subscribe(TOPIC)
        print(f"📡 Suscrito al tópico: {TOPIC}")
    else:
        print(f"❌ Error de conexión. Código: {rc}")


def on_message(client, userdata, msg):
    """
    Callback cuando llega un mensaje MQTT
    Procesa el mensaje y actualiza tanto el cache como el historial
    """
    try:
        # Decodificar payload
        payload = msg.payload.decode()
        data = json.loads(payload)

        # Extraer datos del mensaje
        municipio = data.get("municipio")
        tipo = data.get("tipo")
        valor = data.get("valor")

        # Validar que tenemos los datos necesarios
        if not municipio or not tipo or valor is None:
            print("⚠️  Mensaje incompleto, ignorando...")
            return

        # Normalizar municipio a minúsculas
        municipio = municipio.lower()
        tipo = tipo.lower()

        # Convertir valor a float
        valor = float(valor)

        # Generar timestamp
        timestamp = datetime.now().isoformat()

        # === ACTUALIZAR CACHE (último valor) ===
        if municipio not in latest_data:
            latest_data[municipio] = {}

        latest_data[municipio][tipo] = {
            "valor": valor,
            "timestamp": timestamp
        }

        # === ACTUALIZAR HISTORIAL ===
        if municipio not in historial_data:
            historial_data[municipio] = {}

        if tipo not in historial_data[municipio]:
            # Crear deque con límite máximo de puntos
            historial_data[municipio][tipo] = deque(maxlen=MAX_HISTORY_POINTS)

        # Agregar punto al historial (automáticamente elimina el más viejo si está lleno)
        historial_data[municipio][tipo].append({
            "valor": valor,
            "timestamp": timestamp
        })

        # === ACTUALIZAR LISTA DE MUNICIPIOS ===
        municipios_detectados.add(municipio)

        # Log de confirmación
        historial_size = len(historial_data[municipio][tipo])
        print(f"📊 {municipio.upper()}/{tipo}: {valor} | Historial: {historial_size}/{MAX_HISTORY_POINTS} puntos")

    except json.JSONDecodeError:
        print("❌ Error: Payload no es JSON válido")
    except ValueError:
        print("❌ Error: Valor no es numérico")
    except Exception as e:
        print(f"❌ Error procesando mensaje: {e}")


def on_disconnect(client, userdata, rc):
    """
    Callback cuando se desconecta del broker
    """
    if rc != 0:
        print(f"⚠️  Desconexión inesperada. Código: {rc}")
        print("🔄 Intentando reconectar...")


# === FUNCIONES HELPER PARA ACCEDER A LOS DATOS ===

def get_latest(municipio, tipo=None):
    """
    Obtiene el último valor del cache

    Args:
        municipio (str): Nombre del municipio
        tipo (str, optional): Tipo específico. Si es None, devuelve todos los tipos

    Returns:
        dict: Datos del cache
    """
    municipio = municipio.lower()

    if municipio not in latest_data:
        return {} if tipo is None else None

    if tipo:
        tipo = tipo.lower()
        return latest_data[municipio].get(tipo)

    return latest_data[municipio]


def get_historial(municipio, tipo=None):
    """
    Obtiene el historial de datos

    Args:
        municipio (str): Nombre del municipio
        tipo (str, optional): Tipo específico. Si es None, devuelve todos los tipos

    Returns:
        dict o list: Historial de datos
    """
    municipio = municipio.lower()

    if municipio not in historial_data:
        return {} if tipo is None else []

    if tipo:
        tipo = tipo.lower()
        # Convertir deque a list para JSON serialization
        return list(historial_data[municipio].get(tipo, []))

    # Devolver todo el historial del municipio
    return {
        t: list(hist) for t, hist in historial_data[municipio].items()
    }


def clear_cache(municipio=None):
    """
    Limpia el cache

    Args:
        municipio (str, optional): Si se provee, limpia solo ese municipio
    """
    if municipio:
        municipio = municipio.lower()
        if municipio in latest_data:
            del latest_data[municipio]
            print(f"🗑️  Cache de {municipio} limpiado")
    else:
        latest_data.clear()
        print("🗑️  Todo el cache limpiado")


def clear_historial(municipio=None):
    """
    Limpia el historial

    Args:
        municipio (str, optional): Si se provee, limpia solo ese municipio
    """
    if municipio:
        municipio = municipio.lower()
        if municipio in historial_data:
            del historial_data[municipio]
            print(f"🗑️  Historial de {municipio} limpiado")
    else:
        historial_data.clear()
        print("🗑️  Todo el historial limpiado")


def get_stats():
    """
    Obtiene estadísticas del sistema

    Returns:
        dict: Estadísticas generales
    """
    total_puntos = sum(
        sum(len(hist) for hist in tipos.values())
        for tipos in historial_data.values()
    )

    return {
        "municipios": len(municipios_detectados),
        "total_puntos_historial": total_puntos,
        "max_puntos_por_tipo": MAX_HISTORY_POINTS,
        "municipios_detectados": list(municipios_detectados)
    }


# === INICIALIZACIÓN DEL CLIENTE MQTT ===

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect


def start_mqtt():
    """
    Inicia el cliente MQTT y comienza a escuchar mensajes
    """
    try:
        print(f"🚀 Conectando al broker: {BROKER}:{PORT}")
        client.connect(BROKER, PORT, 60)
        client.loop_start()
        print("✅ Cliente MQTT iniciado en background")
    except Exception as e:
        print(f"❌ Error al iniciar cliente MQTT: {e}")


def stop_mqtt():
    """
    Detiene el cliente MQTT
    """
    client.loop_stop()
    client.disconnect()
    print("🛑 Cliente MQTT detenido")