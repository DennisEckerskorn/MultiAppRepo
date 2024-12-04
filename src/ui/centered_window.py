import customtkinter as ctk
import webbrowser
import subprocess
import os

from services.threads_manager import ThreadsManager
from services.processes_manager import ProcessManager


class CenteredWindow(ctk.CTk):
    def __init__(self, title="MultiApp", width_percentage=0.8, height_percentage=0.8):
        # Inicializacion de la clase:
        super().__init__()

        # Titulo de la ventana:
        self.title(title)

        self.thread_manager = ThreadsManager(self)
        self.process_manager = ProcessManager()

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
        self.create_left_panel()
        self.create_right_panel()
        self.create_center_panel()
        self.create_bottom_bar()
        self.thread_manager.start_threads()

    def create_left_panel(self):
        # Panel izquierdo
        left_panel = ctk.CTkFrame(self, width=200)
        left_panel.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)
        # Secciones y botones
        sections = {
            "Aplicaciones": [
                ("Abrir Chrome", lambda: self.process_manager.open_resource("browser", "https://google.com", "Cannot open browser")),
                ("Visual Studio Code", lambda: self.process_manager.open_resource("program", r"C:\Program Files\Microsoft VS Code\Code.exe", "Can't find VSCode")),
                ("Explorador de Windows", lambda: self.process_manager.open_resource("program", "explorer.exe", "Can't open Windows Explorer")),
                ("Notepad++", lambda: self.process_manager.open_resource("program", r"C:\Program Files\Notepad++\notepad++.exe", "Can't open Notepad++"))
            ]
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

    def dummy_action(self):
        print("Acción no implementada")