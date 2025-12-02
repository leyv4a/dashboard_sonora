import json
import paho.mqtt.client as mqtt

# Cache local para datos del dashboard
latest_data = {}

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "sonora/#"

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)

        municipio = data.get("municipio", "desconocido")
        tipo = data.get("tipo", "desconocido")
        valor = data.get("valor", None)

        latest_data[f"{municipio}_{tipo}"] = valor
        print("Dato recibido:", latest_data)

    except Exception as e:
        print("Error procesando mensaje:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start_mqtt():
    client.connect(BROKER, PORT, 60)
    client.loop_start()
