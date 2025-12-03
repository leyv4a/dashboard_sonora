import json
import paho.mqtt.client as mqtt

# Cache de datos recibidos
latest_data = {}

# Lista dinámica de municipios detectados
municipios_detectados = set()

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

        municipio = data.get("municipio")
        tipo = data.get("tipo")
        valor = data.get("valor")

        if municipio and tipo:
            municipio = municipio.lower()

            # Si el municipio no existe en el diccionario, crearlo
            if municipio not in latest_data:
                latest_data[municipio] = {}

            # Guardar temperatura, humedad, etc.
            latest_data[municipio][tipo] = valor

            # Guardar municipio limpio
            municipios_detectados.add(municipio)

        print("Cache:", latest_data)
        print("Municipios detectados:", municipios_detectados)

    except Exception as e:
        print("Error procesando mensaje:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


def start_mqtt():
    client.connect(BROKER, PORT, 60)
    client.loop_start()
