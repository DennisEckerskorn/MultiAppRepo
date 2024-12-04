import threading
import datetime
import time
import requests
import random

class ThreadsManager:
    def __init__(self, ui_instance):
        self.ui_instance = ui_instance

    def start_threads(self):
        # Hilo para actualizar el reloj
        threading.Thread(target=self.update_time, daemon=True).start()

        # Hilo para actualizar la temperatura
        threading.Thread(target=self.update_temperature, daemon=True).start()

        # Hilo para actualizar correos (simulado)
        threading.Thread(target=self.update_emails, daemon=True).start()

    def update_time(self):
        while True:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            current_date = datetime.datetime.now().strftime('%d/%m/%Y')
            self.ui_instance.after(0, lambda: self.ui_instance.info_labels["hora"].configure(text=f"Hora: {current_time}"))
            self.ui_instance.after(0, lambda: self.ui_instance.info_labels["fecha"].configure(text=f"Fecha: {current_date}"))
            time.sleep(1)

    def update_temperature(self):
        API_KEY = "4ba2b87d7fa32934530b5b4a5a83ebf7"  # Reemplaza con tu clave de OpenWeatherMap
        CITY = "Madrid"  # Cambia por tu ciudad
        while True:
            try:
                temperature = self.get_real_temperature(API_KEY, CITY)
                if temperature is not None:
                    self.ui_instance.after(
                        0,
                        lambda: self.ui_instance.info_labels["temperatura"].configure(text=f"Temperatura local: {temperature}°C")
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

    def update_emails(self):
        count = 0
        while True:
            count += random.randint(0, 2)  # Simula la llegada de 0-2 correos
            self.ui_instance.after(
                0,
                lambda: self.ui_instance.info_labels["emails"].configure(text=f"Correos sin leer: {count}")
            )
            time.sleep(10)  # Actualiza cada 10 segundos
