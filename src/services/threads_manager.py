import datetime
import time
import requests

from src.services.Radio_Player import RadioPlayer
from src.services.scrapper import Scrapper
from src.services.threaden_task import ThreadenTask


class ThreadsManager:
    """Constructor"""

    def __init__(self, ui_instance, email_client):
        self.ui_instance = ui_instance
        self.email_client = email_client
        self.system_monitor = None
        self.radio_player = RadioPlayer()
        self.tasks = {
            "time": ThreadenTask(),
            "temperature": ThreadenTask(),
            "emails": ThreadenTask(),
            "email_client": ThreadenTask(),
            "tetris_game": ThreadenTask(),
            "scrapper": ThreadenTask(),
            "radio_player": ThreadenTask(),
        }
        self.system_monitor_tasks = {}
        self.scrapper = Scrapper(ui_instance)

    def play_radio(self, url):
        """Inicia la reproducción de radio en un hilo."""
        if not self.tasks["radio_player"].running:
            self.tasks["radio_player"].start(self.radio_player.play, url)

    def stop_radio(self):
        """Detiene la reproducción de radio."""
        self.radio_player.stop()

    def set_system_monitor(self, system_monitor):
        """Asigna el monitor del sistema y crea sus tareas"""
        self.system_monitor = system_monitor
        for metric in system_monitor.metrics.keys():
            self.system_monitor_tasks[metric] = ThreadenTask()

    def start_threads(self):
        """Se inician los hilos, Tiempo, Temperatura, Emails"""
        self.tasks["time"].start(self.update_time)
        self.tasks["temperature"].start(self.update_temperature)
        self.tasks["emails"].start(self.update_emails)
        self.tasks["email_client"].start(self.manage_email_client())

        if self.system_monitor:
            for metric in self.system_monitor.metrics.keys():
                self.system_monitor_tasks[metric].start(
                    self.update_system_metric,
                    metric
                )

        if hasattr(self.ui_instance, "tetris_game"):
            self.tasks["tetris_game"].start(self.update_tetris_game)

    def stop_threads(self):
        """Detiene todos los hilos y cierra las conexiones."""
        for name, task in self.tasks.items():
            task.stop()
            print(f"Hilo '{name}' detenido")
            if name == "email_client" and hasattr(self.email_client, "close_connections"):
                self.email_client.close_connections()

        for name, task in self.system_monitor_tasks.items():
            task.stop()
            print(f"Hilo de monitor del sistema '{name}' detenido.")

        if self.system_monitor:
            self.system_monitor.running = False

    def update_tetris_game(self):
        """Ciclo de actualizacion del tetris game"""
        while self.tasks["tetris_game"].running:
            try:
                if self.ui_instance.tetris_game.running and self.ui_instance.tetris_game.winfo_exists():
                    self.ui_instance.tetris_game.update_game()
                time.sleep(0.5)
            except Exception as e:
                print(f"Error en update_tetris_game: {e}")
                break

    def update_system_metric(self, metric):
        """Actualiza una métrica específica del monitor del sistema."""
        while self.system_monitor_tasks[metric].running:
            try:
                self.system_monitor.update_metric(metric)
                time.sleep(self.system_monitor.metrics[metric]["interval"])
            except Exception as e:
                print(f"Error updating metric {metric}: {e}")

    def update_time(self):
        while self.tasks["time"].running:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            current_date = datetime.datetime.now().strftime('%d/%m/%Y')
            self.ui_instance.after(0,
                                   lambda: self.ui_instance.info_labels["hora"].configure(text=f"Hora: {current_time}"))
            self.ui_instance.after(0, lambda: self.ui_instance.info_labels["fecha"].configure(
                text=f"Fecha: {current_date}"))
            time.sleep(1)

    def update_temperature(self):
        API_KEY = "4ba2b87d7fa32934530b5b4a5a83ebf7"  # Reemplaza con tu clave de OpenWeatherMap
        CITY = "Madrid"  # Cambia por tu ciudad
        while self.tasks["temperature"].running:
            try:
                temperature = self.get_real_temperature(API_KEY, CITY)
                if temperature is not None:
                    self.ui_instance.after(
                        0,
                        lambda: self.ui_instance.info_labels["temperatura"].configure(
                            text=f"Temperatura local: {temperature}°C")
                    )
            except Exception as e:
                print(f"Error al obtener la temperatura: {e}")
            time.sleep(600)  # Actualiza cada 10 minutos

    def get_real_temperature(self, api_key, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['main']['temp']  # Retorna la temperatura en °C
        else:
            print(f"Error al obtener la temperatura: {response.status_code}")
            return None

    def manage_email_client(self):
        while self.tasks["email_client"].running:
            try:
                if not self.email_client.is_connected():
                    self.email_client.reconnect()
                time.sleep(10)
            except Exception as e:
                print(f"Error en el EmailClient: {e}")
                time.sleep(10)
            finally:
                self.email_client.close_connections()
                print("Cliente de correo detenido y conexiones cerradas")

    def update_emails(self):
        """Actualiza la cantidad de correos no leídos en tiempo real."""
        while self.tasks["emails"].running:
            try:
                if not self.email_client.is_connected():
                    self.email_client.reconnect()

                if self.email_client.is_connected():
                    unread_count = self.email_client.fetch_unread_count()
                    if self.ui_instance.winfo_exists():  # Verifica si la ventana aún existe
                        self.ui_instance.after(
                            0,
                            lambda: self.ui_instance.info_labels["emails"].configure(
                                text=f"Correos sin leer: {unread_count}"
                            )
                        )
                else:
                    print("No hay conexión al servidor de correo")
            except Exception as e:
                print(f"Error en el hilo de correos: {e}")
            time.sleep(60)

