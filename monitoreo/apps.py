from django.apps import AppConfig


class MonitoreoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoreo'

    def ready(self):
        """
        Este método se ejecuta cuando Django arranca.
        Aquí iniciamos el cliente MQTT automáticamente.
        """
        # Importar solo cuando la app esté lista
        from dashboard.mqtt_client import start_mqtt
        import sys

        # Evitar ejecutar dos veces (Django puede cargar la app dos veces)
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0]:
            try:
                start_mqtt()
                print("🚀 Cliente MQTT iniciado automáticamente")
            except Exception as e:
                print(f"⚠️  Error al iniciar cliente MQTT: {e}")
                print("   El cliente MQTT se puede iniciar manualmente si es necesario")