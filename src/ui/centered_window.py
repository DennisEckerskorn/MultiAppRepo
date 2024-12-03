import customtkinter as ctk
import webbrowser
import subprocess
import os
import threading
import random
import datetime
import time
import requests

class CenteredWindow(ctk.CTk):
    def __init__(self, title="MultiApp", width_percentage=0.8, height_percentage=0.8):
        # Inicializacion de la clase:
        super().__init__()

        # Titulo de la ventana:
        self.title(title)

        # Obtener la resolucion de la pantalla:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcula el tamaño de la ventana según procentaje de la pantalla:
        window_width = int(screen_width * width_percentage)
        window_height = int(screen_height * height_percentage)

        # Calcular la posicion para centrar la ventana:
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        #Configura la ventana
        self.configure_window()

    def configure_window(self):
        # Configuracion de la ventana:
        self.configure(bg_color="lightgray")
        
        #Barra superior con Botones:
        #self.create_menuBar()
        self.create_left_panel()
        self.create_right_panel()
        self.create_center_panel()
        self.create_bottom_bar()
        self.start_threads()

        
    def create_menuBar(self):
        menu_bar = ctk.CTkFrame(self, height=25)
        menu_bar.pack(side=ctk.TOP, fill=ctk.X)

        #Botones del menuBar:
        # Agregar botones de menú
        menus = ["Procesos", "T2.Threads", "T3.Sockets", "T4.Servicios", "T5.Seguridad", "Configuración"]
        for menu in menus:
            btn = ctk.CTkButton(
                menu_bar,
                text=menu,
                command=lambda m=menu: self.on_menu_click(m),
                width=100,
                height=20,
                fg_color="blue",
                hover_color="lightblue"
            )
            btn.pack(side=ctk.LEFT, padx=5, pady=5)

    def create_left_panel(self):
        # Panel izquierdo
        left_panel = ctk.CTkFrame(self, width=200)
        left_panel.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)
        # Secciones y botones
        sections = {
        "": [("Extraer datos", self.dummy_action),
            ("Navegar", self.open_chrome),
            ("Buscar API Google", self.dummy_action)],
            "Aplicaciones": [("Visual Code", self.open_visual_studio_code),
                            ("Windows Explorer", self.open_explorer), ("Notepad++", self.open_notepad_plus)],
        "Procesos batch": [("Copias de seguridad", self.dummy_action)],
        }

        for section, buttons in sections.items():
            if section:
                section_label = ctk.CTkLabel(left_panel, text=section, font=("Arial", 12, "bold"))
                section_label.pack(anchor=ctk.W, pady=5, padx=10)

            for text, command in buttons:
                btn = ctk.CTkButton(left_panel, text=text, command=command, width=150)
                btn.pack(pady=5, padx=10)


    def create_center_panel(self):
        # Panel central con pestañas
        center_panel = ctk.CTkFrame(self)
        center_panel.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=(10, 10), pady=10)

        tab_view = ctk.CTkTabview(center_panel, width=500, height=500)
        tab_view.pack(fill=ctk.BOTH, expand=True)

        tabs = ["Resultados Scrapping", "Navegador", "Correos", "Juego", "Sistema"]
        for tab in tabs:
            tab_view.add(tab)

        # Agregar contenido a las pestañas
        for tab in tabs:
            label = ctk.CTkLabel(tab_view.tab(tab), text=f"Contenido de {tab}", font=("Arial", 12))
            label.pack(pady=10)



    def create_right_panel(self):
        # Panel derecho
        right_panel = ctk.CTkFrame(self, width=250)
        right_panel.pack(side=ctk.RIGHT, fill=ctk.Y, padx=10, pady=10)

        # Chat
        chat_label = ctk.CTkLabel(right_panel, text="Chat", font=("Arial", 14, "bold"), text_color="red")
        chat_label.pack(anchor=ctk.W, pady=5, padx=10)

        chat_box = ctk.CTkTextbox(right_panel, height=100)
        chat_box.pack(fill=ctk.X, padx=10, pady=5)

        send_button = ctk.CTkButton(right_panel, text="Enviar", command=self.dummy_action)
        send_button.pack(pady=5, padx=10)

        # Lista de alumnos
        for i in range(1, 4):
            student_label = ctk.CTkLabel(right_panel, text=f"Alumno {i}", font=("Arial", 12, "bold"), text_color="black")
            student_label.pack(anchor=ctk.W, pady=5, padx=10)

            student_info = ctk.CTkLabel(
                right_panel,
                text="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                wraplength=200,
                justify="left",
            )
            student_info.pack(anchor=ctk.W, padx=10)


    def create_bottom_bar(self):
        # Crear la barra inferior
        self.bottom_bar = ctk.CTkFrame(self, fg_color="lightblue", height=40)
        self.bottom_bar.pack(side=ctk.BOTTOM, fill=ctk.X, padx=0, pady=0)

        # Diccionario para las etiquetas dinámicas
        self.info_labels = {
            "hora": ctk.CTkLabel(self.bottom_bar, text="Hora: --:--:--", font=("Arial", 12), text_color="black"),
            "fecha": ctk.CTkLabel(self.bottom_bar, text="Fecha: --/--/----", font=("Arial", 12), text_color="black"),
            "temperatura": ctk.CTkLabel(self.bottom_bar, text="Temperatura local: --°C", font=("Arial", 12), text_color="black"),
            "emails": ctk.CTkLabel(self.bottom_bar, text="Correos sin leer: 0", font=("Arial", 12), text_color="black"),
        }

        # Empaquetar las etiquetas horizontalmente
        for label in self.info_labels.values():
            label.pack(side=ctk.LEFT, padx=10, pady=5)



    def start_threads(self):
        # Hilo para actualizar el reloj
        threading.Thread(target=self.update_time, daemon=True).start()

        # Hilo para actualizar la temperatura
        threading.Thread(target=self.update_temperature, daemon=True).start()

        # Hilo para actualizar correos (simulado)
        threading.Thread(target=self.update_emails, daemon=True).start()

    def update_time(self):
        # Obtén la hora y la fecha actual
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        current_date = datetime.datetime.now().strftime('%d/%m/%Y')

        # Actualiza las etiquetas en el hilo principal
        self.info_labels["hora"].configure(text=f"Hora: {current_time}")
        self.info_labels["fecha"].configure(text=f"Fecha: {current_date}")

        # Programa la próxima ejecución en 1000 ms (1 segundo)
        self.after(1000, self.update_time)
        
            

    def update_temperature(self):
        # Actualiza la temperatura real cada 10 minutos usando la API de OpenWeatherMap
        API_KEY = "4ba2b87d7fa32934530b5b4a5a83ebf7"  # Reemplaza con tu clave de OpenWeatherMap
        CITY = "Madrid"  # Cambia por tu ciudad
        while True:
            try:
                temperature = self.get_real_temperature(API_KEY, CITY)
                if temperature is not None:
                    self.info_labels["temperatura"].configure(text=f"Temperatura local: {temperature}°C")
            except Exception as e:
                print(f"Error al obtener la temperatura: {e}")
            threading.Event().wait(600)  # Actualiza cada 10 minutos

    def get_real_temperature(self, api_key, city):
        # Función para obtener la temperatura real desde OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['main']['temp']  # Retorna la temperatura en °C
        else:
            print(f"Error al obtener la temperatura: {response.status_code}")
            return None

    def update_emails(self):
        # Simula la actualización de correos no leídos cada 10 segundos
        count = 0
        while True:
            count += random.randint(0, 2)  # Simula la llegada de 0-2 correos
            self.info_labels["emails"].configure(text=f"Correos sin leer: {count}")
            self.after(1000, self.update_time)  # Actualiza cada 10 segundos
            threading.Event().wait(1)

    def dummy_action(self):
        print("Acción no implementada")


    def open_chrome(self):
        try:
            webbrowser.get('chrome').open('https://google.es')
        except:
            webbrowser.open('https://google.es')


    def open_visual_studio_code(self):
        try:
            vs_code_path = r"C:\Program Files\Microsoft VS Code\Code.exe"
            subprocess.Popen([vs_code_path])
        except FileNotFoundError:
            print ("Can't find VSCode")


    def open_explorer(self):
        try:
            subprocess.Popen(['explorer.exe'])
        except:
            print("Can't open Windows Explorer")


    def open_notepad_plus(self):
        try:
            notepad_path = r"C:\Program Files\Notepad++\notepad++.exe"
            subprocess.Popen([notepad_path])
        except:
            print("Can't open NotePad++")



    




